from transformers import AutoTokenizer, AutoModel
import os

def download_models():
    """Download all required models"""
    
    models = [
        "dmis-lab/biobert-base-cased-v1.1",
        "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"
    ]
    
    print("Downloading pre-trained models...")
    print("="*50)
    
    for model_name in models:
        print(f"\n📥 Downloading:  {model_name}")
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            print(f"✅ Successfully downloaded: {model_name}")
        except Exception as e:
            print(f"❌ Error downloading {model_name}: {str(e)}")
    
    print("\n" + "="*50)
    print("✨ Model download complete!")

if __name__ == "__main__":
    download_models()