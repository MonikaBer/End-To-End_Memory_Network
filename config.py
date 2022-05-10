import numpy as np

class BabiConfig(object):
    """
    Configuration for bAbI
    """
    def __init__(self,
        train_story,
        train_questions,
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
        sent_nr
        ):

        self.dictionary       = dictionary
        self.batch_size       = batch_size
        self.nhops            = hops

        if epochs:
            self.nepochs          = epochs
        else:
            self.nepochs          = 100

        if lrate_decay_step:
            self.lrate_decay_step = lrate_decay_step
        else:
            self.lrate_decay_step = 25   # reduce learning rate by half every 25 epochs

        # Use 10% of training data for validation
        nb_questions       = train_questions.shape[1]
        nb_train_questions = int(nb_questions * 0.9)

        self.train_range    = np.array(range(nb_train_questions))
        self.val_range      = np.array(range(nb_train_questions, nb_questions))
        self.enable_time    = RN   # add time embeddings
        self.use_bow        = BoW  # use Bag-of-Words instead of Position-Encoding
        self.linear_start   = LS

        if LW:
            self.share_type     = 2     # layer-wise weight tying
        else:
            self.share_type     = 1     # adjacent weight tying

        self.randomize_time = randomize_time   # amount of noise injected into time index

        self.add_proj       = AP        # add linear layer between internal states
        self.add_nonlin     = NL        # add non-linearity to internal states

        if self.linear_start:
            if ls_nepochs:
                self.ls_nepochs          = ls_nepochs
            else:
                self.ls_nepochs          = 20

            if ls_lrate_decay_step:
                self.ls_lrate_decay_step = ls_lrate_decay_step
            else:
                self.ls_lrate_decay_step = 21

            self.ls_init_lrate       = init_lrate / 2


        if embed_dim == None:
            embed_dim = 20

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


class BabiConfigJoint(object):
    """
    Joint configuration for bAbI
    """
    def __init__(self,
        train_story,
        train_questions,
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
        sent_nr):

        # TODO: Inherit from BabiConfig
        self.dictionary       = dictionary
        self.batch_size       = batch_size
        self.nhops            = hops

        if epochs:
            self.nepochs          = epochs
        else:
            self.nepochs          = 60

        if lrate_decay_step:
            self.lrate_decay_step = lrate_decay_step
        else:
            self.lrate_decay_step = 15   # reduce learning rate by half every 15 epochs

        # Use 10% of training data for validation  # XXX
        nb_questions        = train_questions.shape[1]
        nb_train_questions  = int(nb_questions * 0.9)

        # Randomly split to training and validation sets
        rp = np.random.permutation(nb_questions)
        self.train_range = rp[:nb_train_questions]
        self.val_range   = rp[nb_train_questions:]

        self.enable_time    = RN   # add time embeddings
        self.use_bow        = BoW  # use Bag-of-Words instead of Position-Encoding
        self.linear_start   = LS

        if LW:
            self.share_type     = 2     # layer-wise weight tying
        else:
            self.share_type     = 1     # adjacent weight tying

        self.randomize_time = randomize_time    # amount of noise injected into time index

        self.add_proj       = AP        # add linear layer between internal states
        self.add_nonlin     = NL        # add non-linearity to internal states

        if self.linear_start:
            if ls_nepochs:
                self.ls_nepochs          = ls_nepochs
            else:
                self.ls_nepochs          = 30

            if ls_lrate_decay_step:
                self.ls_lrate_decay_step = ls_lrate_decay_step
            else:
                self.ls_lrate_decay_step = 31

            self.ls_init_lrate       = init_lrate / 2


        if embed_dim == None:
            embed_dim = 50

        # Training configuration
        self.train_config = {
            "init_lrate"   : init_lrate,
            "max_grad_norm": max_grad_norm,
            "in_dim"       : embed_dim,  # XXX:
            "out_dim"      : embed_dim,  # XXX:
            "sz"           : min(sent_nr, train_story.shape[1]),
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
