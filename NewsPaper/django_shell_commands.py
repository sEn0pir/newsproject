from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment


user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')


author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)


category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')


post1 = Post.objects.create(author=author1, post_type='AR', title='Article 1', content='Content of article 1')
post2 = Post.objects.create(author=author2, post_type='AR', title='Article 2', content='Content of article 2')
post3 = Post.objects.create(author=author1, post_type='NW', title='News 1', content='Content of news 1')


PostCategory.objects.create(post=post1, category=category1)
PostCategory.objects.create(post=post1, category=category2)
PostCategory.objects.create(post=post2, category=category3)
PostCategory.objects.create(post=post3, category=category4)


comment1 = Comment.objects.create(post=post1, user=user1, text='Comment 1 on article 1')
comment2 = Comment.objects.create(post=post2, user=user2, text='Comment 1 on article 2')
comment3 = Comment.objects.create(post=post3, user=user1, text='Comment 1 on news 1')
comment4 = Comment.objects.create(post=post1, user=user2, text='Comment 2 on article 1')


post1.like()
post1.like()
post2.dislike()
comment1.like()
comment2.dislike()


author1.update_rating()
author2.update_rating()


best_author = Author.objects.order_by('-rating').first()
print(f"Best author: {best_author.user.username} with rating {best_author.rating}")


best_post = Post.objects.order_by('-rating').first()
print(f"Best post: {best_post.title}, published on {best_post.created_at} by {best_post.author.user.username}, rating: {best_post.rating}, preview: {best_post.preview()}")


comments = Comment.objects.filter(post=best_post)
for comment in comments:
    formatted_date = comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Comment by {comment.user.username} on {formatted_date}, rating: {comment.rating}, text: {comment.text}")