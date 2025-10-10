# AxisTool
```
import QtQuick3D

Node {
    Model {
        source: "#Cylinder"
        eulerRotation.z: 90
        x: 0.5
        scale: Qt.vector3d(0.001, 0.01, 0.001)
        materials: [
            PrincipledMaterial {
                baseColor: "#FF0000"
            }
        ]
    }
    Model {
        source: "#Cylinder"
        y: 0.5
        scale: Qt.vector3d(0.001, 0.01, 0.001)
        materials: [
            PrincipledMaterial {
                baseColor: "#00FF00"
            }
        ]
    }
    Model {
        source: "#Cylinder"
        eulerRotation.x: 90
        z: 0.5
        scale: Qt.vector3d(0.001, 0.01, 0.001)
        materials: [
            PrincipledMaterial {
                baseColor: "#0000FF"
            }
        ]
    }
}
```
# ButtonMenu
```
import QtQuick.Controls
import QtQml.Models

Button {
    id: control
    property ObjectModel items
    onClicked: menu.visible = !menu.visible
    Instantiator {
        model: control.items
        onObjectAdded: (index_, object_) => menu.insertItem(index_, object_)
        onObjectRemoved: (index_, object_) => menu.removeItem(object_)
    }
    Menu {
        id: menu
        y: control.height
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
    }
}
```
# DoubleSpinBox
```
import QtQuick
import QtQuick.Controls

SpinBox {
    id: control
    property int decimals: 2
    readonly property int factor: Math.pow(10, decimals)
    from: decimalToInt(0.0)
    to: decimalToInt(99.0)
    value: decimalToInt(0.0)
    stepSize: decimalToInt(1.0)
    function decimalToInt(v_) {
        return v_ * factor;
    }
    function intToDecimal(v_) {
        return v_ / factor;
    }
    validator: DoubleValidator {
        bottom: control.from
        top: control.to
        locale: control.locale.name
        decimals: control.decimals
        notation: DoubleValidator.StandardNotation
    }
    textFromValue: (value_, locale_) => {
        return Number(value_ / factor).toLocaleString(locale_, 'f', decimals);
    }
    valueFromText: (text_, locale_) => {
        return Number.fromLocaleString(locale_, text_) * factor;
    }
}
```
# JoystickCtrl
```
import QtQuick

Rectangle {
    id: outer
    required property Timer timer
    signal animateXY(double x, double y)
    implicitWidth: inner.width * 4
    implicitHeight: inner.height * 4
    radius: inner.radius * 4
    color: palette.window
    border.color: palette.highlight
    Connections {
        target: outer.timer
        function onTriggered() {
            let x = dragHandler.activeTranslation.x;
            let y = dragHandler.activeTranslation.y;
            if (x === 0 && y === 0) {
                return;
            }
            let r = outer.width / 2;
            x = x > r ? r : (x < -r ? -r : x);
            y = y > r ? r : (y < -r ? -r : y);
            x = x / r;
            y = y / r;
            outer.animateXY(x, y);
        }
    }
    Rectangle {
        id: inner
        width: 50
        height: 50
        radius: 50
        color: palette.highlight
        DragHandler {
            id: dragHandler
            xAxis {
                minimum: 0
                maximum: outer.width - inner.width
            }
            yAxis {
                minimum: 0
                maximum: outer.height - inner.height
            }
        }

        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        states: [
            State {
                when: dragHandler.active
                AnchorChanges {
                    target: inner
                    anchors.horizontalCenter: undefined
                    anchors.verticalCenter: undefined
                }
            }
        ]
    }
}
```
# View3DInputHandler
```
import QtQuick
import QtQuick3D

Item {
    id: root

    required property Node origin
    required property PerspectiveCamera camera

    property vector2d lastPos: Qt.vector2d(0, 0)

    TapHandler {
        id: tapHandler
        target: null
        grabPermissions: PointerHandler.TakeOverForbidden
    }

    DragHandler {
        id: leftBtnDrag
        target: null
        acceptedButtons: Qt.LeftButton
        grabPermissions: PointerHandler.TakeOverForbidden
        onCentroidChanged: {
            if (!active)
                return;
            root.rotateEvent(Qt.vector2d(centroid.position.x, centroid.position.y));
        }
        onActiveChanged: {
            if (active) {
                root.startRotate(Qt.vector2d(centroid.position.x, centroid.position.y));
            } else {
                root.endRotate(Qt.vector2d(centroid.position.x, centroid.position.y));
            }
        }
    }

    DragHandler {
        id: middleBtnDrag
        target: null
        acceptedButtons: Qt.MiddleButton
        acceptedDevices: PointerDevice.Mouse
        grabPermissions: PointerHandler.TakeOverForbidden
        onCentroidChanged: {
            if (!active)
                return;
            root.panEvent(Qt.vector2d(centroid.position.x, centroid.position.y));
        }
        onActiveChanged: {
            if (active) {
                root.startPan(Qt.vector2d(centroid.position.x, centroid.position.y));
            } else {
                root.endPan(Qt.vector2d(centroid.position.x, centroid.position.y));
            }
        }
    }

    PinchHandler {
        id: pinchHandler
        target: null
        grabPermissions: PointerHandler.TakeOverForbidden
        onCentroidChanged: {
            if (!active)
                return;
            root.panEvent(Qt.vector2d(centroid.position.x, centroid.position.y));
        }
        onActiveChanged: {
            if (active) {
                root.startPan(Qt.vector2d(centroid.position.x, centroid.position.y));
            } else {
                root.endPan(Qt.vector2d(centroid.position.x, centroid.position.y));
            }
        }
        onScaleChanged: delta => {
            root.zoomEvent(1 / delta);
        }
    }

    WheelHandler {
        id: wheelHandler
        orientation: Qt.Vertical
        target: null
        acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
        onWheel: event => {
            root.zoomEvent(1 - event.angleDelta.y * 0.001);
        }
    }

    function zoomEvent(factor) {
        camera.z *= factor;
        if (camera.z < 1) {
            camera.clipNear = 0.01;
            camera.clipFar = 100;
            if (camera.z <= 0) {
                camera.z = camera.clipNear;
            }
        } else if (camera.z < 100) {
            camera.clipNear = 0.1;
            camera.clipFar = 1000;
        } else {
            camera.clipNear = 1;
            camera.clipFar = 10000;
        }
    }

    function startRotate(newPos) {
        lastPos = newPos;
    }

    function endRotate(newPos) {
    }

    function rotateEvent(newPos) {
        let delta = newPos.minus(lastPos);
        // rotate x
        let rotateX = delta.x * 0.1;
        rotateX = -rotateX;

        // rotate y
        let rotateY = delta.y * 0.1;
        rotateY = -rotateY;

        origin.rotate(rotateX, origin.up, Node.SceneSpace);
        origin.rotate(rotateY, origin.right, Node.SceneSpace);
        lastPos = newPos;
    }

    function startPan(newPos) {
        lastPos = newPos;
    }

    function endPan(newPos) {
    }

    function panEvent(newPos) {
        let delta = newPos.minus(lastPos);
        delta.x = -delta.x;

        delta.x = (delta.x / width) * camera.z;
        delta.y = (delta.y / height) * camera.z;

        let velocity = Qt.vector3d(0, 0, 0);
        // X Movement
        let xDirection = origin.right;
        velocity = velocity.plus(Qt.vector3d(xDirection.x * delta.x, xDirection.y * delta.x, xDirection.z * delta.x));
        // Y Movement
        let yDirection = origin.up;
        velocity = velocity.plus(Qt.vector3d(yDirection.x * delta.y, yDirection.y * delta.y, yDirection.z * delta.y));

        origin.position = origin.position.plus(velocity);

        lastPos = newPos;
    }
}
```