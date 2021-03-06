from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse
from movie.models import Movie, Watch, Favorite, BelongTo, Produce, Review, ReleaseInfo
from django.contrib.auth.decorators import login_required
from movie.views.MainView import movie_context
from datetime import datetime
from django.db.models import Avg
# Create your views here.
def movie(request, movieid):
	try:
		movie = Movie.objects.get(id__exact=movieid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'movie not found'})
	review_list = Review.objects.filter(mid=movie)
	obj = {}
	rel = BelongTo.objects.filter(mid__exact = movie)
	obj['genre'] = rel
	produce = Produce.objects.filter(mid__exact = movie)
	obj['actors'] = []
	for person in produce:
		if person.cid.crew_type == 0:
			obj['director'] = person.cid.name
		else:
			obj['actors'].append(person.cid.name)
	rev = Review.objects.filter(mid__exact = movie).aggregate(Avg('rating'))
	obj['rating'] = rev['rating__avg']
	if obj['rating'] == None:
		obj['rating'] = 0
	release = ReleaseInfo.objects.filter(mid__exact=movie)
	obj['release'] = release
	context = {'movie': movie,
			   'reviews':review_list,
			   'username': "visitor",
			   'loggedin': False,
			   'request': request
	}
	if request.user.is_authenticated():
		fav = Favorite.objects.filter(uid__exact=request.user, mid__exact=movie)
		if len(fav) == 0:
			obj['isliked'] = False
		else:
			obj['isliked'] = True
		watched = Watch.objects.filter(uid__exact=request.user, mid__exact=movie)
		if len(watched) == 0:
			obj['iswatched'] = False
		else:
			obj['iswatched'] = True
		context['username'] = request.user.username
		context['loggedin'] = True
	context['info'] = obj
	return render(request, 'movie/moviedetail.html', context)

@login_required
def watchmovielist(request):
	movies = []
	watches = Watch.objects.filter(uid__exact=request.user)
	for watch in watches:
		movies.append(watch.mid)
	context = movie_context(request, movies, "watched list")
	return render(request, 'movie/movielist.html', context)

@login_required
def reviewmovie(request, movieid):
	rating = request.POST.get('rating', -1)
	#add error handling here
	review = request.POST.get('review', "")
	movie = Movie.objects.get(id__exact = movieid)
	R = Review(content=review, date=datetime.today(), rating=rating, mid=movie, uid=request.user)
	R.save()
	return redirect("moviedb:movie", movieid=movieid)

@login_required
def deletereview(request, reviewid):
	try:
		review = Review.objects.get(id__exact=reviewid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'review not found'})
	print review.uid.id
	print request.user.id
	if review.uid != request.user:
		return render(request, 'movie/error.html', {'msg': 'illegal delete request'})
	movieid = review.mid.id
	review.delete()
	return redirect("moviedb:movie", movieid=movieid)


@login_required
def watchmovie(request, movieid):
	try:
		movie = Movie.objects.get(id__exact=movieid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'movie not found'})
	watch = Watch(mid=movie, uid=request.user)
	watch.save()
	return redirect("moviedb:movie", movieid=movieid)

@login_required
def unwatchmovie(request, movieid):
	try:
		movie = Movie.objects.get(id__exact=movieid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'movie not found'})
	Watch.objects.filter(mid__exact=movie, uid__exact=request.user).delete()
	return redirect("moviedb:movie", movieid=movieid)

@login_required
def favmovielist(request):
	movies = []
	favs = Favorite.objects.filter(uid__exact=request.user)
	for fav in favs:
		movies.append(fav.mid)
	context = movie_context(request, movies, "favorite list")
	return render(request, 'movie/movielist.html', context)

@login_required
def favmovie(request, movieid):
	try:
		movie = Movie.objects.get(id__exact=movieid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'movie not found'})
	fav = Favorite(mid=movie, uid=request.user)
	fav.save()
	return redirect("moviedb:movie", movieid=movieid)

@login_required
def unfavmovie(request, movieid):
	try:
		movie = Movie.objects.get(id__exact=movieid)
	except Movie.DoesNotExist:
		return render(request, 'movie/error.html', {'msg': 'movie not found'})
	Favorite.objects.filter(mid__exact=movie, uid__exact=request.user).delete()
	return redirect("moviedb:movie", movieid=movieid)
