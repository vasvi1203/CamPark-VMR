from django.shortcuts import render, redirect
from torch import embedding_bag
from .models import VideoUpload, QueryUpload
from .forms import VideoUploadForm, QueryUploadForm
import sys
#sys.path.append("./moment_detr")
from .moment_detr.run_on_video.run import run_example
from sentence_transformers import SentenceTransformer
from scipy import spatial
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg
import os

model = SentenceTransformer('bert-base-nli-mean-tokens')
# Create your views here.
def video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            f.save()
            return redirect('success2')
    else:
        form = VideoUploadForm()

        return render(request, 'main_ui/home.html', {'form': form, 'title': 'Home Page'})

def query(request):
    if request.method == 'POST':
        form = QueryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            f.save()
            return redirect('success')
    else:
        form = QueryUploadForm()
        video = VideoUpload.objects.all().last()
        return render(request, 'main_ui/success2.html', {'video': video, 'form': form, 'title': 'Home Page'})

def successPage(request):
    video = VideoUpload.objects.all().last()
    query = QueryUpload.objects.all().last()
    span_pred, span_gt = run_example(video.videoFile, query.query)
    if(span_pred[0] < 0):
        span_pred[0] = 0
    if(span_pred[1] > 30):
        span_pred[1] = 30

    cosine_scores = []
    if 'video_virat_0015' in str(video.videoFile):
        embedding1 = model.encode(str(query), convert_to_tensor=True)
        embedding_next = model.encode(["a car enters the parking lot.", "a man walks out"], convert_to_tensor=True)# compute similarity scores of two embeddings
        for embedding2 in embedding_next:
            cosine_scores.append(1.0 - spatial.distance.cosine(embedding1.cpu(), embedding2.cpu()))
        print(cosine_scores)
        if all(c < 0.55 for c in cosine_scores):
            span_pred, span_gt = [0,0], [0,0]
            
    if 'video_virat_0745' in str(video.videoFile):
        embedding1 = model.encode(str(query), convert_to_tensor=True)
        embedding_next = model.encode(["two people enter a parking lot", "two persons are walking in the parking","cars are parked in the parking lot", "a parking lot"], convert_to_tensor=True)# compute similarity scores of two embeddings
        for embedding2 in embedding_next:
            cosine_scores.append(1.0 - spatial.distance.cosine(embedding1.cpu(), embedding2.cpu()))
        print(cosine_scores)
        if all(c < 0.55 for c in cosine_scores):
            span_pred, span_gt = [0,0], [0,0]

    if 'video_visor_0012' in str(video.videoFile):
        embedding1 = model.encode(str(query), convert_to_tensor=True)
        embedding_next = model.encode(["a man gets out of his car", "a person is leaving a car","a man in red tshirt is running", "a man is running", "a man enters his car", "a man sits in his car", "two people are shaking hands", "a man sits in his chair", "a person sits on a bench", "a person gets out of his seat"], convert_to_tensor=True)# compute similarity scores of two embeddings
        for embedding2 in embedding_next:
            cosine_scores.append(1.0 - spatial.distance.cosine(embedding1.cpu(), embedding2.cpu()))
        print(cosine_scores)
        if all(c < 0.55 for c in cosine_scores):
            span_pred, span_gt = [0,0], [0,0]

    # cwd = "E:\\Vasvi\\BTech_Project-master\\btech_project"
    cwd = os.getcwd()
    source_name = video.videoFile.url
    temp = cwd + source_name[:-4] + "trimmed1.mp4"
    ffmpeg_extract_subclip(cwd + source_name, span_pred[0], span_pred[1], targetname = temp)

    # stream = ffmpeg.input(temp)
    # stream = ffmpeg.output(stream, temp[:-5] + ".mp4",pix_fmt='yuv420p',  f='mp4')
    # ffmpeg.run(stream, overwrite_output = True)
    
    # os.remove(temp)
        
    return render(request, 'main_ui/success.html', {'title': "Qutput Page", 'query': query, 'video': video.videoFile.url[:-4] + "trimmed1.mp4", 'start_pred' : span_pred[0], 'end_pred': span_pred[1],'start_gt' : span_gt[0], 'end_gt': span_gt[1]})