"""
Image classification program. It uses a pre trained model
to get a score for the presence of wavy clouds in the last recorded photo.
The computed score is added to the data.csv file along with the other entries.
Honestly, it doesn't seem to work so fine, but it's a first try.
The code is wrapped inside a 'chck_wavy_clouds' function it has
a call inside main.py program.
"""

def chck_wavy_clouds(last_img):
    from pathlib import Path
    from PIL import Image
    from pycoral.adapters import common
    from pycoral.adapters import classify
    from pycoral.utils.edgetpu import make_interpreter
    from pycoral.utils.dataset import read_label_file
    
    script_dir = Path(__file__).parent.resolve()
    
    model_file = script_dir/'astropi-wavy-vs-unwavy.tflite' # name of model
    data_dir = script_dir/'data'
    label_file = script_dir/'wavy_vs_unwavy.txt' # Name of your label file
    image_file = script_dir/f'image_{last_img:04d}.jpg' # Name of image for classification
    
    # The following two lines initialize the Coral TPU hardware
    interpreter = make_interpreter(f"{model_file}")
    interpreter.allocate_tensors()
    
    size = common.input_size(interpreter)# checks the size of pictures used to train the model
    image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)# resizes to same sizes of the model training pictures
    
    common.set_input(interpreter, image)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)
    
    labels = read_label_file(label_file)
    for c in classes:
        score = f'{labels.get(c.id, c.id)} {c.score:.5f} image_{last_img:04d}'
    return score