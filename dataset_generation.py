import json
import pandas as pd
from tqdm import tqdm

from react_scripts.react_2 import react_2
from react_scripts.react_6 import react_6
from react_scripts.react_14 import react_14
from react_scripts.react_26 import react_26
from react_scripts.react_30 import react_30
from react_scripts.react_54 import react_54
from react_scripts.react_66 import react_66
from react_scripts.react_70 import react_70
from react_scripts.react_74 import react_74
from react_scripts.react_78 import react_78
from react_scripts.react_94 import react_94

from react_scripts.react12 import compute_react12
from react_scripts.react28 import compute_react28
from react_scripts.react36 import compute_react36
from react_scripts.react72 import compute_react72
from react_scripts.react80 import compute_react80
from react_scripts.react84 import compute_react84

from react_scripts.react3 import compute_react3
from react_scripts.react7 import compute_react7
from react_scripts.react11 import compute_react11
from react_scripts.react23 import compute_react23
from react_scripts.react31 import compute_react31
from react_scripts.react43 import compute_react43
from react_scripts.react59 import compute_react59
from react_scripts.react67 import compute_react67
from react_scripts.react79 import compute_react79
from react_scripts.react99 import compute_react99

from react_scripts.react1 import react_1
from react_scripts.React5 import react_5
from react_scripts.React9 import react_9
from react_scripts.React73 import react_73
from react_scripts.React81 import react_81
from react_scripts.React89 import react_89
from react_scripts.React97 import react_97
from react_scripts.React101 import react_101

with open('github_repos.json', 'r') as file:
    json_data = json.load(file)

dataset = pd.DataFrame()

repo_names = [repo["full_name"] for repo in json_data]
dataset['repo_names'] = repo_names

print(len(dataset))

for func, name in tqdm([
    (react_1, 'react_1'),
    (react_2, 'react_2'),
    (compute_react3, 'react_3'),
    (react_5, 'react_5'),
    (react_6, 'react_6'),
    (compute_react7, 'react_7'),
    (react_9, 'react_9'),
    (compute_react11, 'react_11'),
    (compute_react12, 'react_12'),
    (react_14, 'react_14'),
    (compute_react23, 'react_23'),
    (react_26, 'react_26'),
    (compute_react28, 'react_28'),
    (react_30, 'react_30'),
    (compute_react31, 'react_31'),
    (compute_react36, 'react_36'),
    (compute_react43, 'react_43'),
    (react_54, 'react_54'),
    (compute_react59, 'react_59'),
    (react_66, 'react_66'),
    (compute_react67, 'react_67'),
    (react_70, 'react_70'),
    (compute_react72, 'react_72'),
    (react_73, 'react_73'),
    (react_74, 'react_74'),
    (react_78, 'react_78'),
    (compute_react79, 'react_79'),
    (compute_react80, 'react_80'),
    (react_81, 'react_81'),
    (compute_react84, 'react_84'),
    (react_89, 'react_89'),
    (react_94, 'react_94'),
    (react_97, 'react_97'),
    (compute_react99, 'react_99'),
    (react_101, 'react_101'),
]):
    dataset[name] = dataset['repo_names'].apply(lambda x: func(x))

# print(dataset)
dataset.to_csv('dataset.csv', index=False)
