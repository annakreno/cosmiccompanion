Plutonic Rockets blasting off again!

Anna / Andrew / Sarven


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_events = models.ManyToManyField(Event)
    def __str__(self):
        return f"{self.get_user_display()}"


in view.py, to create a user profile, maybe add the below to the function that creates a new user signup function??:

profile = UserProfile.objects.create(user=user)
to retrieve a user's profile.. 
    user = User.objects.get(username='john')
    profile = UserProfile.objects.get(user=user)
    saved_events = Event.objects.filter
