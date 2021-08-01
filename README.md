# face-symmetrizer

```python
from face_symmetrizer import FaceSym

f = FaceSym("https://pbs.twimg.com/media/E7jaibgUcAUWvg-?format=jpg") # Image URL or local file path
# ATTR: ['image_location',
         'f_img', 'f_img_PIL', 'image_size',
         'face_locations', 'face_landmarks',
         'mid_face_locations', 'face_count']
```

```python
f.get_full_image(show=True) #=> <PIL.Image.Image>
```

```python
f.get_face_box_drawed_image(show=True) #=> <PIL.Image.Image>
```

```python
f.get_cropped_face_images(show=True) #=> [<PIL.Image.Image>, ...]
```

```python
f.get_symmetrized_images(show=True) #=> (left_cropped, left_cropped_inner, left_cropped_outer,
                                         right_cropped, right_cropped_inner, right_cropped_outer)
```
