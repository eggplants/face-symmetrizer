from face_symmetrizer import FaceSym

f = FaceSym("img/two_people.jpg")
# or:
# f = FaceSym("https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/two_people.jpg")
for k in  ['image_location',
           'f_img', 'f_img_PIL', 'image_size',
           'face_locations', 'face_landmarks',
           'mid_face_locations', 'face_count']:
    print(k+":", f.__getattribute__(k))

print("show an full image")
f.get_full_image(show=True)

print("show an image facebox drawed")
f.get_face_box_drawed_image(show=True)

print("show cropped face(s)")
f.get_cropped_face_images(show=True)

print("show symmetrized images")
for i in range(f.face_count):
    f.get_symmetrized_images(idx=i, show=True)
