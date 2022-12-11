from pathlib import Path

from src.evaluation.evaluator import PokemonEvaluator

# The class used for the evaluation of the users' submissions.
EVALUATOR_CLASS = PokemonEvaluator
EVALUATOR_KWARGS = {}

# The directory in which the users' submissions will be saved
SUBMISSIONS_DIR = Path(__file__).parent.parent.absolute() / 'user_submissions'

# The name of the encrypted passwords file
PASSWORDS_DB_FILE = Path(__file__).parent.parent.absolute() / 'passwords.db'
ARGON2_KWARGS = {}

# Maximum number of users allowed in the system. If None, no limitation is enforced.
MAX_NUM_USERS = None

# The extension type required for a submission file (e.g. ".json"). If None, any extension is allowed.
ALLOWED_SUBMISSION_FILE_EXTENSION = 'csv'

SHOW_TOP_K_ONLY = 50000

ADMIN_USERNAME = '5!g4I'
