import numpy as np

class BabiConfig(object):
    """
    Configuration for bAbI
    """
    def __init__(self,
        train_story,
        dictionary,
        epochs,
        hops,
        LS,
        RN,
        BoW,
        LW,
        NL,
        batch_size,
        lrate_decay_step,
        randomize_time,
        AP,
        ls_nepochs,
        ls_lrate_decay_step,
        init_lrate,
        max_grad_norm,
        embed_dim,
        sent_nr,
        results_path
        ):

        self.results_path = results_path

        self.dictionary = dictionary
        self.batch_size = batch_size
        self.nhops = hops
        self.nepochs = epochs
        self.lrate_decay_step = lrate_decay_step    # reduce learning rate by half every 25 epochs

        self.enable_time = RN   # add time embeddings
        self.use_bow = BoW  # use Bag-of-Words instead of Position-Encoding
        self.linear_start = LS

        if LW:
            self.share_type = 2     # layer-wise weight tying
        else:
            self.share_type = 1     # adjacent weight tying

        self.randomize_time = randomize_time   # amount of noise injected into time index

        self.add_proj = AP        # add linear layer between internal states
        self.add_nonlin = NL        # add non-linearity to internal states

        if self.linear_start:
            self.ls_nepochs = ls_nepochs
            self.ls_lrate_decay_step = ls_lrate_decay_step
            self.ls_init_lrate = init_lrate / 2

        # Training configuration
        self.train_config = {
            "init_lrate"   : init_lrate,
            "max_grad_norm": max_grad_norm,
            "in_dim"       : embed_dim,
            "out_dim"      : embed_dim,
            "sz"           : min(sent_nr, train_story.shape[1]),  # number of sentences
            "voc_sz"       : len(self.dictionary),
            "bsz"          : self.batch_size,
            "max_words"    : len(train_story),
            "weight"       : None
        }

        if self.linear_start:
            self.train_config["init_lrate"] = self.ls_init_lrate

        if self.enable_time:
            self.train_config.update({
                "voc_sz"   : self.train_config["voc_sz"] + self.train_config["sz"],
                "max_words": self.train_config["max_words"] + 1  # Add 1 for time words
           })


    def split_sets(self, train_questions):
        # Use 10% of training data for validation
        nb_questions = train_questions.shape[1]
        nb_train_questions = int(nb_questions * 0.9)
        # Split to training and validation sets
        self.train_range = np.array(range(nb_train_questions))
        self.val_range = np.array(range(nb_train_questions, nb_questions))


class BabiConfigJoint(BabiConfig):
    """
    Joint configuration for bAbI
    """
    def __init__(self,
        train_story,
        dictionary,
        epochs,
        hops,
        LS,
        RN,
        BoW,
        LW,
        NL,
        batch_size,
        lrate_decay_step,
        randomize_time,
        AP,
        ls_nepochs,
        ls_lrate_decay_step,
        init_lrate,
        max_grad_norm,
        embed_dim,
        sent_nr,
        results_path):

        super(BabiConfigJoint, self).__init__(
            train_story,
            dictionary,
            epochs,
            hops,
            LS,
            RN,
            BoW,
            LW,
            NL,
            batch_size,
            lrate_decay_step,
            randomize_time,
            AP,
            ls_nepochs,
            ls_lrate_decay_step,
            init_lrate,
            max_grad_norm,
            embed_dim,
            sent_nr,
            results_path
        )


    def split_sets(self, train_questions):
        # Use 10% of training data for validation
        nb_questions = train_questions.shape[1]
        nb_train_questions = int(nb_questions * 0.9)
        # Split to training and validation sets
        rp = np.random.permutation(nb_questions)
        self.train_range = rp[:nb_train_questions]
        self.val_range   = rp[nb_train_questions:]
