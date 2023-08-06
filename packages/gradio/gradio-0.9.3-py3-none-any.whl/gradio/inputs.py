"""
This module defines various classes that can serve as the `input` to an interface. Each class must inherit from
`AbstractInput`, and each class must define a path to its template. All of the subclasses of `AbstractInput` are
automatically added to a registry, which allows them to be easily referenced in other parts of the code.
"""

from abc import ABC, abstractmethod
from gradio import preprocessing_utils, validation_data
import numpy as np
import PIL.Image, PIL.ImageOps
import time
import warnings
import json
import datetime

# Where to find the static resources associated with each template.
# BASE_INPUT_INTERFACE_TEMPLATE_PATH = 'static/js/interfaces/input/{}.js'
BASE_INPUT_INTERFACE_JS_PATH = 'static/js/interfaces/input/{}.js'


class AbstractInput(ABC):
    """
    An abstract class for defining the methods that all gradio inputs should have.
    When this is subclassed, it is automatically added to the registry
    """
    def __init__(self, label):
        self.label = label

    def get_validation_inputs(self):
        """
        An interface can optionally implement a method that returns a list of examples inputs that it should be able to
        accept and preprocess for validation purposes.
        """
        return []

    def get_template_context(self):
        """
        :return: a dictionary with context variables for the javascript file associated with the context
        """
        return {"label": self.label}

    def sample_inputs(self):
        """
        An interface can optionally implement a method that sends a list of sample inputs for inference.
        """
        return []

    def preprocess(self, inp):
        """
        By default, no pre-processing is applied to text.
        """
        return inp

    @classmethod
    def get_shortcut_implementations(cls):
        """
        Return dictionary of shortcut implementations
        """
        return {}

    def rebuild_flagged(self, dir, msg):
        """
        All interfaces should define a method that rebuilds the flagged input when it's passed back (i.e. rebuilds image from base64)
        """
        pass


class Sketchpad(AbstractInput):
    def __init__(self, cast_to="numpy", shape=(28, 28), invert_colors=True,
                 flatten=False, scale=1/255, shift=0,
                 dtype='float64', sample_inputs=None, label=None):
        self.image_width = shape[0]
        self.image_height = shape[1]
        self.invert_colors = invert_colors
        self.flatten = flatten
        self.scale = scale
        self.shift = shift
        self.dtype = dtype
        self.sample_inputs = sample_inputs
        super().__init__(label)

    def preprocess(self, inp):
        """
        Default preprocessing method for the SketchPad is to convert the sketch to black and white and resize 28x28
        """
        im_transparent = preprocessing_utils.decode_base64_to_image(inp)
        im = PIL.Image.new("RGBA", im_transparent.size, "WHITE")  # Create a white background for the alpha channel
        im.paste(im_transparent, (0, 0), im_transparent)
        im = im.convert('L')
        if self.invert_colors:
            im = PIL.ImageOps.invert(im)
        im = im.resize((self.image_width, self.image_height))
        if self.flatten:
            array = np.array(im).flatten().reshape(1, self.image_width * self.image_height)
        else:
            array = np.array(im).flatten().reshape(1, self.image_width, self.image_height)
        array = array * self.scale + self.shift
        array = array.astype(self.dtype)
        return array

    # TODO(abidlabs): clean this up
    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method to decode a base64 image
        """

        im = preprocessing_utils.decode_base64_to_image(msg)

        timestamp = datetime.datetime.now()
        filename = f'input_{timestamp.strftime("%Y-%m-%d-%H-%M-%S")}.png'
        im.save(f'{dir}/{filename}', 'PNG')
        return filename

    def get_sample_inputs(self):
        encoded_images = []
        if self.sample_inputs is not None:
            for input in self.sample_inputs:
                if self.flatten:
                    input = input.reshape((self.image_width, self.image_height))
                if self.invert_colors:
                    input = 1 - input
                encoded_images.append(preprocessing_utils.encode_array_to_base64(input))
        return encoded_images


class Webcam(AbstractInput):
    def __init__(self, image_width=224, image_height=224, num_channels=3, label=None):
        self.image_width = image_width
        self.image_height = image_height
        self.num_channels = num_channels
        super().__init__(label)

    def get_validation_inputs(self):
        return validation_data.BASE64_COLOR_IMAGES

    @classmethod
    def get_shortcut_implementations(cls):
        return {
            "webcam": {},
        }

    def preprocess(self, inp):
        """
        Default preprocessing method for is to convert the picture to black and white and resize to be 48x48
        """
        im = preprocessing_utils.decode_base64_to_image(inp)
        im = im.convert('RGB')
        im = preprocessing_utils.resize_and_crop(im, (self.image_width, self.image_height))
        array = np.array(im).flatten().reshape(self.image_width, self.image_height, self.num_channels)
        return array

    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method to decode a base64 image
        """
        inp = msg['data']['input']
        im = preprocessing_utils.decode_base64_to_image(inp)
        timestamp = datetime.datetime.now()
        filename = f'input_{timestamp.strftime("%Y-%m-%d-%H-%M-%S")}.png'
        im.save(f'{dir}/{filename}', 'PNG')
        return filename


class Textbox(AbstractInput):
    def __init__(self, sample_inputs=None, lines=1, placeholder=None, label=None, numeric=False):
        self.sample_inputs = sample_inputs
        self.lines = lines
        self.placeholder = placeholder
        self.numeric = numeric
        super().__init__(label)

    def get_validation_inputs(self):
        return validation_data.ENGLISH_TEXTS

    def get_template_context(self):
        return {
            "lines": self.lines,
            "placeholder": self.placeholder,
            **super().get_template_context()
        }

    @classmethod
    def get_shortcut_implementations(cls):
        return {
            "text": {},
            "textbox": {"lines": 7},
            "number": {"numeric": True}
        }

    def preprocess(self, inp):
        """
        Cast type of input
        """
        if self.numeric:
            return float(inp)
        else:
            return inp

    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method for text saves it .txt file
        """
        return json.loads(msg)

    def get_sample_inputs(self):
        return self.sample_inputs


class Radio(AbstractInput):
    def __init__(self, choices, label=None):
        self.choices = choices
        super().__init__(label)

    def get_template_context(self):
        return {
            "choices": self.choices,
            **super().get_template_context()
        }


class Dropdown(AbstractInput):
    def __init__(self, choices, label=None):
        self.choices = choices
        super().__init__(label)

    def get_template_context(self):
        return {
            "choices": self.choices,
            **super().get_template_context()
        }


class CheckboxGroup(AbstractInput):
    def __init__(self, choices, label=None):
        self.choices = choices
        super().__init__(label)

    def get_template_context(self):
        return {
            "choices": self.choices,
            **super().get_template_context()
        }


class Slider(AbstractInput):
    def __init__(self, minimum=0, maximum=100, label=None):
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(label)

    def get_template_context(self):
        return {
            "minimum": self.minimum,
            "maximum": self.maximum,
            **super().get_template_context()
        }

    @classmethod
    def get_shortcut_implementations(cls):
        return {
            "checkbox": {},
        }


class Checkbox(AbstractInput):
    def __init__(self, label=None):
        super().__init__(label)

    @classmethod
    def get_shortcut_implementations(cls):
        return {
            "checkbox": {},
        }


class Image(AbstractInput):
    def __init__(self, cast_to=None, shape=(224, 224, 3), image_mode='RGB',
                 scale=1/127.5, shift=-1, cropper_aspect_ratio=None, label=None):
        self.cast_to = cast_to
        self.image_width = shape[0]
        self.image_height = shape[1]
        self.num_channels = shape[2]
        self.image_mode = image_mode
        self.scale = scale
        self.shift = shift
        self.cropper_aspect_ratio = "false" if cropper_aspect_ratio is None else cropper_aspect_ratio
        super().__init__(label)

    def get_validation_inputs(self):
        return validation_data.BASE64_COLOR_IMAGES

    @classmethod
    def get_shortcut_implementations(cls):
        return {
            "image": {},
        }

    def get_template_context(self):
        return {
            'aspect_ratio': self.cropper_aspect_ratio,
            **super().get_template_context()
        }

    def cast_to_base64(self, inp):
        return inp

    def cast_to_im(self, inp):
        return preprocessing_utils.decode_base64_to_image(inp)

    def cast_to_numpy(self, inp):
        im = self.cast_to_im(inp)
        arr = np.array(im).flatten()
        return arr

    def preprocess(self, inp):
        """
        Default preprocessing method for is to convert the picture to black and white and resize to be 48x48
        """
        cast_to_type = {
            "base64": self.cast_to_base64,
            "numpy": self.cast_to_numpy,
            "pillow": self.cast_to_im
        }
        if self.cast_to:
            return cast_to_type[self.cast_to](inp)

        im = preprocessing_utils.decode_base64_to_image(inp)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            im = im.convert(self.image_mode)

        im = preprocessing_utils.resize_and_crop(im, (self.image_width, self.image_height))
        im = np.array(im).flatten()
        im = im * self.scale + self.shift
        if self.num_channels is None:
            array = im.reshape(self.image_width, self.image_height)
        else:
            array = im.reshape(self.image_width, self.image_height, \
                                self.num_channels)
        return array

    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method to decode a base64 image
        """
        im = preprocessing_utils.decode_base64_to_image(msg)
        timestamp = datetime.datetime.now()
        filename = f'input_{timestamp.strftime("%Y-%m-%d-%H-%M-%S")}.png'
        im.save(f'{dir}/{filename}', 'PNG')
        return filename

    # TODO(abidlabs): clean this up
    def save_to_file(self, dir, img):
        """
        """
        timestamp = time.time()*1000
        filename = 'input_{}.png'.format(timestamp)
        img.save('{}/{}'.format(dir, filename), 'PNG')
        return filename


class CSV(AbstractInput):

    def get_name(self):
        return 'csv'

    def preprocess(self, inp):
        """
        By default, no pre-processing is applied to a CSV file (TODO:aliabid94 fix this)
        """
        return inp

    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method for csv
        """
        return json.loads(msg)


class Microphone(AbstractInput):

    def preprocess(self, inp):
        """
        By default, no pre-processing is applied to a microphone input file
        """
        file_obj = preprocessing_utils.decode_base64_to_wav_file(inp)
        mfcc_array = preprocessing_utils.generate_mfcc_features_from_audio_file(file_obj.name)
        return mfcc_array

    def rebuild_flagged(self, dir, msg):
        """
        Default rebuild method for csv
        """
        return json.loads(msg)


# Automatically adds all shortcut implementations in AbstractInput into a dictionary.
shortcuts = {}
for cls in AbstractInput.__subclasses__():
    for shortcut, parameters in cls.get_shortcut_implementations().items():
        shortcuts[shortcut] = cls(**parameters)
