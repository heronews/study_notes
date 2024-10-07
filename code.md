# WebSocket
```
#ifndef WEBSOCKET_CLIENT_H
#define WEBSOCKET_CLIENT_H

#include <QCborArray>
#include <QCborMap>
#include <QCborValue>
#include <QThread>
#include <QWebSocket>

class websocket_client : public QObject
{
    Q_OBJECT
public:
    static websocket_client &instance()
    {
        static websocket_client client;
        return client;
    }

signals:
    void connected();
    void disconnected();
public slots:
    void open(const QUrl &url);
    void close();
    void send_text_message(const QString &message);
    void send_binary_message(const QByteArray &message);

private:
    explicit websocket_client(QObject *parent = nullptr);
    ~websocket_client();
    websocket_client(const websocket_client &) = delete;
    void operator=(const websocket_client &) = delete;

private:
    QWebSocket *websocket;
    QThread thread;
};

#endif // WEBSOCKET_CLIENT_H
```
```
#include "websocket_client.h"

websocket_client::websocket_client(QObject *parent)
    : QObject(parent)
    , websocket(nullptr)
{
    moveToThread(&thread);
    websocket = new QWebSocket();
    websocket->moveToThread(&thread);
    connect(websocket, &QWebSocket::textMessageReceived, this, [](const QString &message) {});
    connect(websocket, &QWebSocket::binaryMessageReceived, this, [this](const QByteArray &message) {});
    connect(websocket, &QWebSocket::connected, this, &websocket_client::connected);
    connect(websocket, &QWebSocket::disconnected, this, &websocket_client::disconnected);
    connect(&thread, &QThread::finished, websocket, &QObject::deleteLater);
    thread.start();
}

websocket_client::~websocket_client()
{
    thread.quit();
    thread.wait();
}

void websocket_client::open(const QUrl &url)
{
    websocket->open(url);
}

void websocket_client::close()
{
    websocket->close();
}

void websocket_client::send_text_message(const QString &message)
{
    websocket->sendTextMessage(message);
}

void websocket_client::send_binary_message(const QByteArray &message)
{
    websocket->sendBinaryMessage(message);
}
```
ButtonMenu.qml
```
import QtQuick
import QtQuick.Controls 2.15
import QtQml 2.15

Button {
    property ObjectModel items
    id: control
    onClicked: menu.visible = !menu.visible
    Instantiator {
        model: items
        onObjectAdded: (index, object) => menu.insertItem(index, object)
        onObjectRemoved: (index, object) => menu.removeItem(object)
    }
    Menu {
        id: menu
        y: control.height
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
    }
}
```
DoubleSpinBox.qml
```
import QtQuick
import QtQuick.Controls 2.15

SpinBox {
    id: control
    property int decimals: 2
    readonly property int factor: Math.pow(10, decimals)
    from: toInt(0.0)
    to: toInt(99.0)
    value: toInt(0.0)
    stepSize: toInt(1.0)
    function toInt(v) {
        return v * factor
    }
    function toDouble(v) {
        return v / factor
    }
    validator: DoubleValidator {
        bottom: control.from
        top: control.to
        locale: control.locale.name
        decimals: control.decimals
    }
    textFromValue: function (value, locale) {
        return Number(control.value / control.factor).toLocaleString(
                    locale, 'f', control.decimals)
    }
    valueFromText: function (text, locale) {
        return Number.fromLocaleString(locale, text) * control.factor
    }
}
```
