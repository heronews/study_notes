# fastapi jwt
user.py
```
class UserBase(SQLModel):
    username: str

class User(UserBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    password: str
```
dependencies.py
```
sql_engine = create_engine("sqlite:///database.db", echo=True)

def get_sql_session():
    with Session(sql_engine) as session:
        yield session

sql_session_dep = Annotated[Session, Depends(get_sql_session)]

crypt_context = CryptContext(schemes=["bcrypt"])
```
users.py
```
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

KEY = "0f6600d243b9ae3d788727e74d81654ccdaca2042c1872c28323e017d6edba3d"

async def get_current_user(session: sql_session_dep, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, KEY, ["HS256"])
        db_user = session.exec(select(User).where(User.username == payload["sub"])).one()
        return db_user
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="auth failed")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def users(session: sql_session_dep, offset: int = 0, limit : int = 100):
    return session.exec(select(User).offset(offset).limit(limit)).all()

@router.post("/register")
async def register(session: sql_session_dep, user: User):
    user.password = crypt_context.hash(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login")
async def login(session: sql_session_dep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = session.exec(select(User).where(User.username == form_data.username)).one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login failed")
    if not crypt_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login failed")
    payload = {
        "sub": db_user.username,
        "exp": datetime.now() + timedelta(minutes=1)
    }
    return {"access_token":jwt.encode(payload, KEY, "HS256"), "token_type":"bearer"}

@router.post("/me")
async def me(session: sql_session_dep, user: User = Depends(get_current_user)):
    return user

@router.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    with open(f"./{file.filename}", "wb") as f:
        f.write(content)
    return ""
```
# fastapi cors
```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
# fastapi docs
```
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory=Path(static.__file__).parent), name="static")

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_oauth2_redirect_html():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
```
# fastapi etc
```
Field(validation_alias=AliasChoices("id", "_id"))

pipeline = [
    {
        "$set": {
            key: {"$mergeObjects": ["$key", new_value]}
        }
    }
]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="", env_file=".env", env_file_encoding="utf-8"
    )
```
# pyproject.toml
```
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages]
find = {}

[tool.setuptools.package-data]
"package.static" = ["*.js", "*.css"]

[project]
name = "package"
version = "0.0.1"
dependencies = []

[project.scripts]
project_cli = "package.main:main"
```


