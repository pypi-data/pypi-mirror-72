# Author: Herilalaina Rakotoarison

import requests


class OpenDL():
    """Utility class to allow easy push and pull on OpenDL server.

    Parameters
    ----------
    hostname : string
        Hostname of OpenDL server.

    """
    link_grammar = "/grammar"
    link_string = "/string"
    link_check_string = "/check_grammar_string"
    link_perf = "/performance"
    link_perfs = "/performances"
    link_dataset = "/dataset"

    def __init__(self, hostname, grammar_name, dataset_name):
        """Init method.

        Parameters
        ----------
        hostname : string
            Hostname of OpenDL server.
        grammar_name : string
            Name of grammar. It may be a simple github link.
        """
        self.hostname = hostname
        self.grammar_id = self._get_grammar_id(grammar_name=grammar_name)
        self.grammar_name = grammar_name
        self.dataset_id = self._get_dataset_id(dataset_name=dataset_name)
        self.dataset_name = dataset_name

    def _get_grammar_id(self, grammar_name):
        res = requests.post(self.hostname + self.link_grammar,
                            json={"grammar_name": grammar_name})
        if "message" in res and res["message"] == "Internal Server Error":
            raise Exception("Error when setting up grammar")
        else:
            result = res.json()
            self.grammar_id = result["grammar_id"]
            self.grammar_name = grammar_name
            return self.grammar_id

    def _get_dataset_id(self, dataset_name):
        res = requests.post(self.hostname + self.link_dataset,
                            json={"dataset_name": dataset_name})
        if "message" in res and res["message"] == "Internal Server Error":
            raise Exception("Error when setting up grammar")
        else:
            result = res.json()
            return result["dataset_id"]

    def _create_new_string(self, word):
        if not hasattr(self, "grammar_id"):
            raise Exception("You need to setup your grammar!!")

        res = requests.post(self.hostname + self.link_string,
                            json={"grammar_id": self.grammar_id, "string_name": word})
        if "message" in res and res["message"] == "Internal Server Error":
            raise Exception("Error when setting up string")
        else:
            result = res.json()
            return result["string_id"]

    def pull_performances(self, word, max_results=-1):
        """Get the stored performance string.

        Parameters
        ----------
        word : str
            Description of string.
        max_results : int
            Max number of result to return.

        Returns
        -------
        type: array of execution. execution: {
                            string_id:int
                            array of performance {epoch:int,
                                                  value:float,
                                                  subset:int,
                                                  runtime:float,
                                                  metric name:string}
                            }
        """
        if not hasattr(self, "grammar_id"):
            raise Exception("You need to setup your grammar!!")

        res = requests.post(self.hostname + self.link_check_string, json={"grammar_id": self.grammar_id, "word": word, "limit": max_results})
        if "message" in res and res["message"] == "Internal Server Error":
            raise Exception("Error when setting up string")
        else:
            return res.json()

    def push_performances(self, word, performances):
        """Add new performance to the corresponding string and dataset.

        Parameters
        ----------
        word : str
            Definition of the word.
        performances: array of dict(epoch:int, value:float, subset:int, metric_name:string)
            List of performance. Ex: [{'epoch': 1, 'metric_name': 'accuracy', 'runtime': 1.0, 'subset': 0, 'value': 0.25}
                                        {"epoch": 2, "value": 0.7, "subset": 0, "metric_name": "accuracy", 'runtime': 0.0},
                                        {"epoch": 3, "value": 0.8, "subset": 0, "metric_name": "accuracy", 'runtime': 4.0}]

        Returns
        -------
        type: dict(status:string)
            Ex. success.

        """
        string_id = self._create_new_string(word)
        print(string_id)
        perf = {
            "string_id": string_id,
            "dataset_id": self.dataset_id,
            "performances": performances
        }
        res = requests.post(self.hostname + self.link_perfs, json=perf)
        return res.json()


# import requests
# server = openDL("localhost:5000")
# grammar_id = server.get_grammar_id("Default GramNAS Grammar")
# dataset_id = server.get_dataset_id("CIFAR-10")
# string_perf = server.pull_performances("conv; conv; conv")

# performances: [{"epoch": 1, "value": 0.6, "subset": 0, "metric_name": "accuracy"}, {"epoch": 2, "value": 0.7, "subset": 0, "metric_name": "accuracy"}, {"epoch": 3, "value": 0.8, "subset": 0, "metric_name": "accuracy"}]
# res = requests.post('http://127.0.0.1:5000/performances', json={"string_id":1, "dataset_id": 1, "performances": [{"epoch": 1, "value": 0.6, "subset": 0, "metric_name": "accuracy"}, {"epoch": 2, "value": 0.7, "subset": 0, "metric_name": "accuracy"}, {"epoch": 3, "value": 0.8, "subset": 0, "metric_name": "accuracy"}]})


# TODO: init(hostname:str, grammar_name:str, dataset_name:str)
# TODO: pull_performances(word: str) -> array of execution. execution: string_id:int + array of performance {epoch ...}.
# TODO: push_performances(word: str, array of performance)
