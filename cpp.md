# write las file
```
laszip_POINTER laszip_writer = nullptr;
if (laszip_create (&laszip_writer))
  {
    return;
  }
laszip_header *header;
laszip_get_header_pointer (laszip_writer, &header);
header->version_major = 1;
header->version_minor = 4;
header->header_size = 375;
header->offset_to_point_data = 375;
header->point_data_format = 6;
header->point_data_record_length = 30;
if (laszip_open_writer (laszip_writer, file_name.c_str (), 0))
  {
    return;
  }
laszip_point *point;
if (laszip_get_point_pointer (laszip_writer, &point))
  {
    return;
  }
laszip_F64 coordinates[3];
coordinates[0] = p.x;
coordinates[1] = p.y;
coordinates[2] = p.z;
if (laszip_set_coordinates (laszip_writer, coordinates))
  {
    return;
  }
if (laszip_write_point (laszip_writer))
  {
    return;
  }
if (laszip_update_inventory (laszip_writer))
  {
    return;
  }
laszip_close_writer (laszip_writer);
laszip_destroy (laszip_writer);
```
# thread pool
```
#include <atomic>
#include <condition_variable>
#include <functional>
#include <future>
#include <iostream>
#include <queue>
#include <thread>
#include <vector>

class thread_pool
{
public:
  thread_pool (size_t count) : count_ (count), stop_ (false)
  {
    for (size_t i = 0; i < count_; ++i)
      {
        workers_.emplace_back ([this] () {
          while (true)
            {
              std::function<void ()> task;
              {
                std::unique_lock<std::mutex> lock (mtx_);
                cv_.wait (lock, [this] {
                  return stop_.load () || !tasks_.empty ();
                });
                if (stop_.load ())
                  break;
                task = std::move (tasks_.front ());
                tasks_.pop ();
              }
              task ();
            }
        });
      }
  }

  ~thread_pool ()
  {
    stop_.store (true);
    cv_.notify_all ();
    for (auto &i : workers_)
      {
        i.join ();
      }
  }

  template <typename Fn, typename... Args>
  auto
  enqueue (Fn &&fn, Args &&...args)
  {
    using return_type = std::invoke_result_t<Fn, Args...>;

    auto task = std::make_shared<std::packaged_task<return_type ()> > (
        std::bind (std::forward<Fn> (fn), std::forward<Args> (args)...));

    std::future<return_type> res = task->get_future ();
    {
      std::unique_lock<std::mutex> lock (mtx_);
      tasks_.emplace ([task] () { (*task) (); });
    }
    cv_.notify_one ();
    return res;
  }

private:
  size_t count_;
  std::vector<std::thread> workers_;
  std::atomic_bool stop_;

  std::queue<std::function<void ()> > tasks_;
  std::mutex mtx_;
  std::condition_variable cv_;
};

class event_loop
{
public:
  event_loop () : stop_ (false) {}
  ~event_loop () {}

  void
  post_task (const std::function<void ()> &task)
  {
    {
      std::unique_lock<std::mutex> lock (mtx_);
      tasks_.emplace (task);
    }
    cv_.notify_one ();
  }

  void
  run ()
  {
    stop_.store (false);
    while (true)
      {
        std::function<void ()> task;
        {
          std::unique_lock<std::mutex> lock (mtx_);
          cv_.wait (lock,
                    [this] { return stop_.load () || !tasks_.empty (); });
          if (stop_.load ())
            break;
          task = std::move (tasks_.front ());
          tasks_.pop ();
        }
        task ();
      }
  }

  void
  stop ()
  {
    stop_.store (true);
    cv_.notify_all ();
  }

private:
  std::atomic_bool stop_;

  std::queue<std::function<void ()> > tasks_;
  std::mutex mtx_;
  std::condition_variable cv_;
};
```
# QtQuick Custom Geometry
```
setPrimitiveType(QQuick3DGeometry::PrimitiveType::Points);
setStride(sizeof(float) * 7);
addAttribute(QQuick3DGeometry::Attribute::PositionSemantic,
              0,
              QQuick3DGeometry::Attribute::F32Type);
addAttribute(QQuick3DGeometry::Attribute::ColorSemantic,
              sizeof(float) * 3,
              QQuick3DGeometry::Attribute::F32Type);

addAttribute(QQuick3DGeometry::Attribute::IndexSemantic,
              0,
              QQuick3DGeometry::Attribute::U32Type);
```
```
QByteArray vertex_data;
vertex_data.resize(sizeof(float) * 7 * cloud->size());
float *vp = reinterpret_cast<float *>(vertex_data.data());

QByteArray index_data;
index_data.resize(sizeof(uint32_t) * cloud->size());
uint32_t *ip = reinterpret_cast<uint32_t *>(index_data.data());

uint32_t i = 0;
for (auto &p : cloud->points) {
    *(vp + 0) = p.x;
    *(vp + 1) = p.y;
    *(vp + 2) = p.z;
    *(vp + 3) = p.r / 255.0;
    *(vp + 4) = p.g / 255.0;
    *(vp + 5) = p.b / 255.0;
    *(vp + 6) = p.a / 255.0;
    vp += 7;

    *ip++ = i++;
}
setVertexData(vertex_data);
setIndexData(index_data);
update();

// (std::clamp(v, min, max) - min) / (max - min);
// color.setHsvF(startHue + hue * i, 1.0, 1.0);
```
# Rosbridge
```
#include <QCborValue>
#include <QJsonDocument>
#include <QThread>
#include <QWebSocket>
#include <qqmlintegration.h>

class WebSocketClient : public QObject {
  Q_OBJECT
  QML_ELEMENT
  QML_UNCREATABLE("create by cpp")
public:
  static WebSocketClient &instance() {
    static WebSocketClient client;
    return client;
  }

signals:
  void connected();
  void disconnected();
public slots:
  void msgDispatch(const QVariantMap &var);

  void open(const QUrl &url);
  void close();
  void sendTextMessage(const QString &message);
  void sendBinaryMessage(const QByteArray &message);

private:
  explicit WebSocketClient(QObject *parent = nullptr);
  ~WebSocketClient();
  WebSocketClient(const WebSocketClient &) = delete;
  void operator=(const WebSocketClient &) = delete;

private:
  QWebSocket *websocket;
  QThread thread;
};

class Subscriber : public QObject {
  Q_OBJECT
  QML_ELEMENT
  QML_UNCREATABLE("create by cpp")
public:
  inline static QMap<QString, Subscriber *> subscribers;
  Subscriber(const QString &topic, const QString &type, int queue_length,
             const QString &compression, QObject *parent = nullptr)
      : QObject(parent) {
    id_ = QUuid::createUuid().toString();
    topic_ = topic;
    type_ = type;
    queue_length_ = queue_length;
    compression_ = compression;
    subscribers[topic_] = this;
  }
  ~Subscriber() { subscribers.remove(topic_); }

public slots:
  void subscribe() {
    QVariantMap var({{"op", "subscribe"},
                     {"id", id_},
                     {"topic", topic_},
                     {"type", type_},
                     {"queue_length", queue_length_},
                     {"compression", compression_}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }
  void unsubscribe() {
    QVariantMap var({{"op", "unsubscribe"},
                     {"id", id_},
                     {"topic", topic_},
                     {"type", type_}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }

private:
  QString id_;
  QString topic_;
  QString type_;
  int queue_length_;
  QString compression_;

signals:
  void readyHandle(const QVariantMap &var);
};

class Publisher : public QObject {
  Q_OBJECT
  QML_ELEMENT
  QML_UNCREATABLE("create by cpp")
public:
  Publisher(const QString &topic, const QString &type,
            QObject *parent = nullptr)
      : QObject(parent) {
    id_ = QUuid::createUuid().toString();
    topic_ = topic;
    type_ = type;
  }
  ~Publisher() {}

public slots:
  void advertise() {
    QVariantMap var(
        {{"op", "advertise"}, {"id", id_}, {"topic", topic_}, {"type", type_}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }
  void unadvertise() {
    QVariantMap var({{"op", "unadvertise"}, {"id", id_}, {"topic", topic_}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }
  void publish(const QVariantMap &msg) {
    QVariantMap var(
        {{"op", "publish"}, {"id", id_}, {"topic", topic_}, {"msg", msg}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }

private:
  QString id_;
  QString topic_;
  QString type_;
};

class ServiceClient : public QObject {
  Q_OBJECT
  QML_ELEMENT
  QML_UNCREATABLE("create by cpp")
public:
  inline static QMap<QString, ServiceClient *> service_clients;
  ServiceClient(const QString &service, const QString &compression,
                QObject *parent = nullptr)
      : QObject(parent) {
    id_ = QUuid::createUuid().toString();
    service_ = service;
    compression_ = compression;
    service_clients[id_] = this;
  }
  ~ServiceClient() { service_clients.remove(id_); }

public slots:
  void callService(const QVariantMap &args) {
    QVariantMap var({{"op", "call_service"},
                     {"id", id_},
                     {"service", service_},
                     {"args", args},
                     {"compression", compression_}});
    QByteArray text = QJsonDocument::fromVariant(var).toJson();
    WebSocketClient::instance().sendTextMessage(text);
  }

private:
  QString id_;
  QString service_;
  QString compression_;

signals:
  void readyHandle(const QVariantMap &var);
};
```
```
WebSocketClient::WebSocketClient(QObject *parent)
    : QObject(parent), websocket(nullptr) {
  websocket = new QWebSocket();
  websocket->moveToThread(&thread);
  connect(websocket, &QWebSocket::textMessageReceived, this,
          [this](const QString &message) {
            emit msgDispatch(
                QJsonDocument::fromJson(message.toUtf8()).toVariant().toMap());
          });
  connect(websocket, &QWebSocket::binaryMessageReceived, this,
          [this](const QByteArray &message) {
            emit msgDispatch(QCborValue::fromCbor(message).toVariant().toMap());
          });
  connect(websocket, &QWebSocket::connected, this, &WebSocketClient::connected);
  connect(websocket, &QWebSocket::disconnected, this,
          &WebSocketClient::disconnected);
  connect(&thread, &QThread::finished, websocket, &QObject::deleteLater);
  thread.start();
}

WebSocketClient::~WebSocketClient() {
  thread.quit();
  thread.wait();
}

void WebSocketClient::msgDispatch(const QVariantMap &var) {
  QString op = var["op"].toString();
  if (op == "publish") {
    QString topic = var["topic"].toString();
    if (Subscriber::subscribers.contains(topic)) {
      emit Subscriber::subscribers[topic]->readyHandle(var);
    }
  } else if (op == "service_response") {
    QString id = var["id"].toString();
    if (ServiceClient::service_clients.contains(id)) {
      emit ServiceClient::service_clients[id]->readyHandle(var);
    }
  }
}

void WebSocketClient::open(const QUrl &url) {
  QMetaObject::invokeMethod(websocket, "open", Q_ARG(QUrl, url));
}

void WebSocketClient::close() { QMetaObject::invokeMethod(websocket, "close"); }

void WebSocketClient::sendTextMessage(const QString &message) {
  QMetaObject::invokeMethod(
      websocket, [this, message]() { websocket->sendTextMessage(message); });
}

void WebSocketClient::sendBinaryMessage(const QByteArray &message) {
  QMetaObject::invokeMethod(
      websocket, [this, message]() { websocket->sendBinaryMessage(message); });
}
```