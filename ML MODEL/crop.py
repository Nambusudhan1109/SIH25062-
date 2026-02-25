import kagglehub

# Download latest version
path = kagglehub.model_download("adnanosman19/crop-recomendationmodel/scikitLearn/default")

print("Path to model files:", path)