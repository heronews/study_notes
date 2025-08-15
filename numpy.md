# numpy ros pointcloud
```
arr = numpy.frombuffer(
    msg.data,
    [
        ("x", "f4"),
        ("y", "f4"),
        ("z", "f4"),
        ("homogeneous", "f4"),
        ("pad", f"V{msg.point_step - 16}"),
    ],
)
arr = structured_to_unstructured(arr[["x", "y", "z", "homogeneous"]])
T = numpy.array(tf, numpy.dtype("f4")).reshape(4, 4)
numpy.dot(arr, T.T)

arr = numpy.concatenate(arrs, 0)
PointCloud2(
    header=Header(),
    height=1,
    width=arr.shape[0],
    fields=[
        PointField(
            name="x", offset=0, datatype=PointField.FLOAT32, count=1
        ),
        PointField(
            name="y", offset=4, datatype=PointField.FLOAT32, count=1
        ),
        PointField(
            name="z", offset=8, datatype=PointField.FLOAT32, count=1
        ),
    ],
    point_step=16,
    row_step=arr.shape[0],
    data=arr.tobytes(),
)
```
