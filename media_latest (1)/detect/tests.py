from django.test import TestCase

# Create your tests here.
# Load model directly
from transformers import AutoModel
model = AutoModel.from_pretrained("Arena/FakeNews-Detection")
