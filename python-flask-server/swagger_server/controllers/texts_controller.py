import connexion
import six
import json
from swagger_server.models.text import Text  # noqa: E501
from swagger_server import util

from transformers import AutoConfig, AutoTokenizer, AutoModel
from summarizer import Summarizer
#model_name = 'nlpaueb/legal-bert-base-uncased'
model_name = 'facebook/bart-large-cnn'
#download the model from HuggingFace
custom_config = AutoConfig.from_pretrained(model_name)
custom_config.output_hidden_states=True
custom_tokenizer = AutoTokenizer.from_pretrained(model_name)
custom_model = AutoModel.from_pretrained(model_name, config=custom_config)
bert_legal_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
print('Using model {}\n'.format(model_name))

bert_legal_model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)

def add_text(body):  # noqa: E501
    """Add a new text

     # noqa: E501

    :param body: Text data
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        if connexion.request.is_json:
            body = Text.from_dict(connexion.request.get_json())
            summary = bert_legal_model(body.text, min_length=8, ratio=0.05)
            data = {'text': summary}
            return json.dumps(data)
        return

