import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Veri yolu
train_dir = 'path/to/train_dataset'
validation_dir = 'path/to/validation_dataset'

# Veri artırma ve ön işleme
train_datagen = ImageDataGenerator(rescale=1.0/255.0, validation_split=0.2)
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)
