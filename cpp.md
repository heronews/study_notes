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