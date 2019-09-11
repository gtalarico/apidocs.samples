# ApiDocs.co - Code Search Sample

### How Does it Work?

[Apidocs.co](https://apidocs.co) uses the Github Code Search API against this repo to provide Code Samples directly within pages.

Because the Github Code Search API is limited to a single user or repo, this repository aggregates multiple relevant repos so they can all be searchable in a single request.

### Limitations

* It's plain text search &ndash; some generic names like `Application` can trigger many false positives
* It's limited to certain entity types (e.g., `Class`, `Method`, `Property`, etc.)

### How to Contribute?

* Fork this repo
* Add a relevant repo to `repos.json`
* Run `python update.py`
* Send a [Pull Request](https://github.com/gtalarico/apidocs.samples/pulls)
