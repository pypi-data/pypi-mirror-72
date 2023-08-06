from .branch import Branch
from .event import Event
from .file import File
from .plan import Plan
from .update import Update
from .run import Run

import openai.object_classes

# Monkey-patch new classes into openai-python
openai.object_classes.OBJECT_CLASSES.update(
    {"branch": Branch, "plan": Plan, "update": Update, "event": Event}
)
