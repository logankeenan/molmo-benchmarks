# Running Locally

* create the virtual env `python3 -m venv venv`
* active it `source venv/bin/activate`
* install dep `pip install -r requirements.txt`

# Results

Memory Usage

* allenai/Molmo-7B-O-0924
    * with bits and bytes - 14184MiB / 24564MiB
    * without bits and bytes - 18314MiB / 24564MiB
* allenai/Molmo-7B-D-0924
    * with bits and bytes - 12796MiB / 24564MiB
    * without bits and bytes - 18388MiB / 24564MiB

# Conclusion

**4090**
Reducing the image size does reduce the generation time. Reducing it more than 50% appears will reduce the accuracy.
This was mainly around the "login link". The image text is "log in", so maybe that had an impact.
allenai/Molmo-7B-O-0924 is the faster model, but with a trade-off of more memory.

* Questions, does spelling accuracy in the text prompt improve results? If I specify "Name" rather than "name" since "
  Name" is what appears in the image.
* What if I asked for all the coordinates in a single large prompt?
  * I imagine this would be faster, but would it be accurate?
* Is there better image compression that would work better?
