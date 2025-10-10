# vscode clangd 配置
在CMakeLists.txt中添加`set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`生成compile_commands.json文件
```
{
    "clangd.path": "/usr/bin/clangd",
    "clangd.arguments": [
        "--compile-commands-dir=${workspaceFolder}/build",
        "--log=error",
        "--all-scopes-completion",
        "--completion-style=bundled",
        "--background-index",
        "--clang-tidy",
        "--fallback-style=GNU",
        "-j=8",
        "--pch-storage=memory",
        "--header-insertion=never"
    ]
}
```
# vcpkg 配置
```
Launch-VsDevShell.ps1 -Arch amd64
$env:LOCALAPPDATA="D:\"
vcpkg.exe new --application
vcpkg.exe add port qt
```