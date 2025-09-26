#!/bin/bash

# Install spaCy model for NLP processing
python -m spacy download en_core_web_sm

# Any other post-deployment setup can go here
echo "Post-deployment setup completed"