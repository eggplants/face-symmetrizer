def scan_known_people(known_people_folder): ...
def print_result(filename, name, distance, show_distance: bool = ...) -> None: ...
def test_image(image_to_check, known_names, known_face_encodings, tolerance: float = ..., show_distance: bool = ...) -> None: ...
def image_files_in_folder(folder): ...
def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance) -> None: ...
def main(known_people_folder, image_to_check, cpus, tolerance, show_distance) -> None: ...