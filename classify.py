from pathlib import Path
from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file

script_dir = Path(__file__).parent.resolve()

model_file = script_dir/'models'/'astropi-wavy-vs-unwavy.tflite' # name of model
data_dir = script_dir/'data'
label_file = data_dir/'wavy_vs_unwavy.txt' # Name of your label file
image_file = data_dir/'tests'/'zz_astropi_1_photo_116.jpg' # Name of image for classification

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
    print(f'{labels.get(c.id, c.id)} {c.score:.5f}')