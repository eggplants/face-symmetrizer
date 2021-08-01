# face-symmetrizer

- Easy symmetrizer for an image contained face(s)

## Install

```bash
pip install face_symmetrizer
```

## How

- First, load an image

```python
from face_symmetrizer import FaceSym

f = FaceSym("img/two_people.jpg") # Image URL or local file path
# ATTR: ['image_location',
         'f_img', 'f_img_PIL', 'image_size',
         'face_locations', 'face_landmarks',
         'mid_face_locations', 'face_count']
```

- Get & show a full image

```python
f.get_full_image(show=True) #=> <PIL.Image.Image>
```

![fig1](img/Figure_1.png)

- Get & show an image of a rectangle drawn around a face.

```python
f.get_face_box_drawed_image(show=True) #=> <PIL.Image.Image>
```

![fig2](img/Figure_2.png)

- Get & show cropped face(s)

```python
f.get_cropped_face_images(show=True) #=> [<PIL.Image.Image>, ...]
```

![fig3](img/Figure_3.png)
![fig4](img/Figure_4.png)

- Get & show symmetrized images (face: 0)

```python
f.get_symmetrized_images(show=True, idx=0) #=> (left_cropped, left_cropped_inner, left_cropped_outer,
                                         right_cropped, right_cropped_inner, right_cropped_outer)
```

![fig1](img/Figure_5.png)

- Get & show symmetrized images (face: 1)

```python
f.get_symmetrized_images(show=True, idx=1)
```

![fig1](img/Figure_6.png)
