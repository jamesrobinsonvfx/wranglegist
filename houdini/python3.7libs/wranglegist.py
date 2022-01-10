"""Submit code snippets to Gist"""
import json
import os
import re
import requests

try:
    import hou
except ImportError:
    # Running elsewhere (cli tests probably)
    pass

GIST_API = "https://api.github.com/gists"
GIST_URL = "https://gist.github.com"
VALID_EXTENSIONS = [".h", ".vfl", ".c", ".cl", ".py"]
VISIBILITY_TAGS = ("private", "public")


class GistError(Exception):
    """Custom Error for our Gist interactions."""

    def __init__(self, message):
        super(GistError, self).__init__(message)
        self.message = message

    def __str__(self):
        return "{0}\nAborting...".format(self.message)


class GitHubAuth:
    """Authenticate user and token from the file on disk."""

    def __init__(self, user=None, token=None):
        """Setup this GitHubAuth instance.

        :param user: GitHub username, defaults to None
        :type user: str, optional
        :param token: Personal Access Token, defaults to None
        :type token: str, optional
        """
        if user and token:
            self.user = user
            self.token = token
        else:
            auth = self._auth()
            self.user = auth[0]
            self.token = auth[1]

    def __str__(self):
        return "User: {0} Token: {1}".format(self.user, self.token)

    @staticmethod
    def _auth():
        """Process the token file.

        :raises GistError: If token doesn't exist, or the file is empty
        :return: User, Token tuple
        :rtype: 2-tuple of str
        """
        home = os.path.expanduser("~")
        tokenfile = os.path.join(home, "gist_personal_access_token")
        if not os.path.isfile(tokenfile):
            raise GistError(
                "Unable to locate personal access token at "
                "~/gist_personal_access_token. "
                "Are you sure you created one?"
            )
        user = ""
        token = ""
        with open(tokenfile, "r") as file_:
            user = file_.readline().rstrip()
            token = file_.read().rstrip()

        if not token:
            raise GistError(
                "Token file is empty. "
                "Please make sure you copied and pasted the token "
                "string from GitHub!"
            )
        return (user, token)


class GistRequest:
    """Request for posting the Gist."""

    def __init__(self, auth, gist):
        """Setup this GistRequest instance.

        :param auth: Authorization object
        :type auth: :class:`.GitHubAuth`
        :param gist: Gist to submit
        :type gist: :class:`.Gist`
        """
        self.auth = auth
        self.gist = gist
        self.url = GIST_API
        self.headers = {
            "X-Github-Username": self.auth.user,
            "Content-type": "application/json",
            "Authorization": "token {0}".format(self.auth.token)
        }

    def data(self):
        """Data dict to send in the request to the GitHub API.

        Built from the :class:`.Gist` instance passed to this object.

        :return: Data dictionary
        :rtype: dict
        """
        return {
            "description": self.gist.desc,
            "public": self.gist.public,
            "files": {self.gist.filename: {"content": self.gist.snippet}}
        }

    def post(self):
        """Use the GitHub API to POST the gist.

        :return: Response from the API
        :rtype: :class:`requests.Response`
        """
        response = requests.post(
            self.url,
            data=json.dumps(self.data()),
            headers=self.headers,
            timeout=60.0
        )
        return response

    @property
    def auth(self):
        """GitHub authentication.

        :param auth: Authentican object with `user` and `token` attribs
        :type auth: :class:`.GitHubAuth`
        :raises TypeError: Must be a :class:`.GitHubAuth instance`
        """
        return self._auth

    @auth.setter
    def auth(self, auth):
        if not isinstance(auth, GitHubAuth):
            raise TypeError("Must be of type <GitHubAuth>.")
        self._auth = auth

    @property
    def gist(self):
        return self._gist

    @gist.setter
    def gist(self, gist):
        """Gist to submit.

        :param gist: Filled-out Gist object
        :type gist: :class:`.Gist`
        :raises TypeError: Must be a :class:`.Gist` instance
        """
        if not isinstance(gist, Gist):
            raise TypeError("Must be of type <Gist>.")
        self._gist = gist


class Gist:
    """Container to hold and validate user attribs to push to Gist."""

    def __init__(self, filename, ext, desc, snippet, visibility="public"):
        """Setup this Gist instance.

        :param filename: What to call the file in Gist
        :type filename: str
        :param ext: File type. Leading `.` can be omitted
        :type ext: str
        :param desc: Short description of the gist
        :type desc: str
        :param snippet: Code snippet to submit, defaults to None
        :type snippet: str, optional
        :param visibility: Visibility level.
            Options are "public" and "private". Defaults to "public"
        :type visibility: str, optional
        """
        self.ext = ext
        self.visibility = visibility
        self.filename = filename
        self.desc = desc
        self.snippet = snippet
        self.public = True

    @property
    def filename(self):
        """Sanitzed filename.

        :param name: What to call the file in Gist
        :type name: str
        :raises GistError: Cannot be an empty string
            or contain illegal phrases
        """
        return self._name

    @filename.setter
    def filename(self, name):
        if not name:
            raise GistError("Filename cannot be an empty string!")
        illegal = [r"gistfile\d+"]
        for term in illegal:
            if re.match(term, name):
                raise GistError("Gist files cannot contain {0}".format(term))
        self._name = "{0}{1}".format("_".join(name.split()), self.ext)

    @property
    def ext(self):
        """Sanitized file extension.

        :param extension: File type. Must be in VAlID_EXTENSIONS
        :type extension: str
        :raises GistError: Not a valid extension
        """
        return self._ext

    @ext.setter
    def ext(self, extension):
        if not extension.startswith("."):
            extension = ".{0}".format(extension)

        if extension not in VALID_EXTENSIONS:
            raise GistError(
                "Extension must be one of the following: {0}".format(
                    " ".join(VALID_EXTENSIONS)
                )
            )
        self._ext = extension

    @property
    def desc(self):
        """Sanitized description.

        :param description: Short description of the snippet
        :type description: str
        """
        return self._desc

    @desc.setter
    def desc(self, description):
        try:
            self._desc = (description[0].upper() + description[1:]).rstrip(".")
        except IndexError:
            self._desc = description

    @property
    def snippet(self):
        """Code snippet.

        :param code: Code snippet to submit
        :type code: str
        :raises GistError: Can't be empty
        """
        return self._snippet

    @snippet.setter
    def snippet(self, code):
        if not code:
            raise GistError("Snippet cannot be empty!")
        self._snippet = code

    @property
    def visibility(self):
        """Visibility level of the Gist.

        Take a string since the default hou ui only has string inputs.
        We'll set the `public` bool for the request here.

        :param viz: Visibility level. Options are "public" and "private"
        :type viz: str
        :raises ValueError: Must be a valid visibility string
        """
        return self._visibility

    @visibility.setter
    def visibility(self, viz):
        if not viz.lower() in VISIBILITY_TAGS:
            raise ValueError(
                "Invalid visibility selection. "
                "Options are {0} without the quotes).".format(
                    " ".join(["\"{0}\"".format(x) for x in VISIBILITY_TAGS])
                )
            )
        self._visibility = viz
        self.public = bool(VISIBILITY_TAGS.index(viz))


class GistErrorHandler:
    """Custom error handler to raise dialogs when in the Houdini UI."""

    def __init__(self, err):
        """Setup this GistErrorHandler instance.

        :param err: Exception to handle
        :type err: :class:`.GistError`
        """
        self.err = err
        self.context = self._get_context()

        # Handle it right after being initialized
        self.handle()

    def handle(self):
        """Adjust behavior based on context.

        When running on the commandline for testing, use regular
        `raise` and traceback. When in a Houdini UI session, raise
        user-friendly dialogs instead.

        :raises self.err: Error to handle
        """
        if self.context in ("cli", "hou"):
            raise self.err

        # Catch the exception
        if self.context == "hou_ui":
            # Redirect the message to a displayMessage
            hou.ui.displayMessage(
                self.err.message,
                title="Gist Submission Error",
                severity=hou.severityType.Error
            )

    @property
    def err(self):
        return self._err

    @err.setter
    def err(self, exception):
        """Exception to handle.

        :param exception: Exception to handle
        :type exception: :class:`.GistError`
        :raises TypeError: Must be a :class:`.GistError` instance
        """
        if not isinstance(exception, GistError):
            raise TypeError("Handler can only handle <GistError>s")
        self._err = exception

    @staticmethod
    def _get_context():
        """Determine where the script is running.

        :return: Context. One of `hou`, `hou.ui` or `cli`
        :rtype: str
        """
        context = "cli"
        try:
            import hou
            context = "hou"
            if hou.isUIAvailable():
                context = "hou_ui"
        except ImportError:
            pass
        return context


def guess_filename(node):
    """Infer a filename for the Gist based on the node's name.

    If the node hasn't been renamed, return an empty string.

    :param node: Node the snippet comes from
    :type node: :class:`hou.Node`
    :return: Suggested filename
    :rtype: str
    """
    if not re.match(
        r"{0}\d*".format(node.type().nameComponents()[2]),
        node.name()
    ):
        return node.name()
    else:
        return ""


def guess_filetype(parm):
    """Infer a filetype from the snippet parameter.

    If the `editorlang` key exists, try that first. Otherwise, try to
    guess based on the node's type. If neither match well, return an
    empty string.

    :param parm: Paramter containing the snippet
    :type parm: :class:`hou.Parm`
    :return: Suggested file extension
    :rtype: str
    """
    exts = {
        "python": ".py",
        "vex": ".h",
        "opencl": ".cl",
    }

    editorlang = parm.parmTemplate().tags().get("editorlang")
    if editorlang:
        return exts[editorlang.lower()]

    # Try by node type
    type_map = {
        "wrangle": exts["vex"],
        "python": exts["python"],
        "opencl": exts["opencl"]
    }
    for searchterm, ext in type_map.items():
        if searchterm in parm.node().type().nameComponents()[2]:
            return ext
    return ""


def auto_populate_desc(snippet):
    """Create a description based on the first line comment.

    If the first line of the snippet starts with a comment, use that
    comment to create a description string. Otherwise, return an empty
    string.

    :param snippet: Snippet to derive description from
    :type snippet: str
    :return: Description string
    :rtype: str
    """
    singleline = ("//", "#")
    multiline = ("/\*", "\'\'\'", "\"\"\"")
    comment_tokens = [x for y in [singleline, multiline] for x in y]
    match = re.match(r"^({0})(.*)".format("|".join(comment_tokens)), snippet)
    if not match:
        return ""
    desc = ""
    token = match.group(1)
    if token in singleline:
        # Grab everything up til a newline char
        try:
            desc = re.match(r"{0}(.*?(?=\n))".format(token), snippet).group(1)
        except AttributeError:
            pass
    elif token in multiline:
        desc = re.match(r"{0}([\w\W]*?){1}".format(
            token, token[::-1]), snippet).group(1).replace("\n", " ")

    return desc.rstrip().lstrip()


def create(parm):
    """Collect user info about the Gist and POST it to GitHub.

    :param parm: Parameter containing the snippet
    :type parm: :class:`hou.Parm`
    """
    node = parm.node()
    snippet = parm.evalAsString()

    initial_contents = [
        guess_filename(node),
        guess_filetype(parm),
        auto_populate_desc(snippet),
        "public"
    ]

    content = hou.ui.readMultiInput(
        "Add Gist options",
        ("Filename", "File Type", "Description", "Visibility"),
        buttons=("Cancel", "OK"),
        default_choice=1,
        close_choice=0,
        help="Visiblity options are \"public\" and \"private\"",
        title="Create Gist",
        initial_contents=initial_contents
    )
    if not content[0]:
        return
    content = list(content[1])
    content.insert(-1, snippet)  # Get it in the right position

    # Intantiate a Gist object
    try:
        gist = Gist(*content)
        gist_request = GistRequest(GitHubAuth(), gist)
    except GistError as err:
        GistErrorHandler(err)
        # Early return, don't raise in a hou ui session (annoying)
        return

    try:
        response = gist_request.post()
    except:
        # Raise our own exception to prevent houdini from crashing
        GistErrorHandler(GistError(
            "Unable to push to GitHub. "
            "Please ensure your personal access token exists and is not "
            "expired, and that your username is typed correctly."
        ))
    if response.ok:
        link = "{0}/{1}/{2}".format(
            GIST_URL,
            gist_request.auth.user,
            response.json()["id"]
        )
        hou.ui.displayMessage(
            "Created Gist. See link below.",
            title="Success!",
            details_label="Show Link",
            details_expanded=True,
            details=link
        )
    else:
        print(response.json())
        hou.ui.displayMessage(
            "Unable to create gist.",
            title="Fail",
            severity=hou.severityType.Error
        )


# Command line testing
if __name__ == "__main__":
    gist = Gist("testfile", "py", "a test", "public", "some code here")
    # gist = Gist("", "py", "a test", "public", "some code here")
    auth = GitHubAuth()
    req = GistRequest(auth, gist)
    print(GitHubAuth())
    print(req.data())
    try:
        response = req.post()
        print(
            "Success\nGist Posted at "
            "{0}/{1}/{2}\n".format(req.url, req.auth.user,
                                   response.json()["id"]),
            "Exiting."
        )
        print(response.json())
    except Exception as err:
        print(err)
