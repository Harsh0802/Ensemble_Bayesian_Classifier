# Ensemble_Bayesian_Classifier
This study evaluated two different Bayesian classifiers; tree augmented Naive Bayes
and Markov blanket estimation networks in order to build an ensemble model for
prediction the severity of breast masses. The objective of the proposed algorithm was
to help physicians in their decisions to perform a breast biopsy on a suspicious lesion
seen in a mammogram image or to perform a short term follow-up examination
instead. While, mammography is the most effective and available tool for breast cancer
screening, mammograms do not detect all breast cancers. Also, a small portion of
mammograms show that a cancer could probably be present when it is not (called a
false-positive result).

Naive Bayes (NB):
Naïve-Bayes is bayesian classifier (more of a supervise learning algorithm) which
uses the fact that the events contributing to the final target class (i.e. output) are
mutually independent i.e. we relax the constraint of dependence of the events (the
dependent variables) which is the usual trend followed in Bayesian classifiers. The NB
is an extension of the bayes theorem.

Tree Augmented Naive Bayes (TAN):
TAN is an improvement over the naive Bayes model as it allows for each attribute
to depend on another attribute in addition to the target attribute. The class attribute is
the single parent of each node of a NB network: TAN considers adding a second parent
to each attribute; the predictive attributes are allowed to point to each other (as long as
no cycles are introduced). The decision to add these edges between attributes is made
on the basis of a specific goodness of fit measure, such as Maximum Likelihood
(ML).] This method associates a weight to each edge corresponding to the mutual
information between the two variables. The TAN learning procedure is as follows:
• Build the tree-like network structure over the predictive attribute X by using the
maximum weighting spanning tree
• Add Y as a parent of every Xi where 1≤i≤n
• Estimate the parameter of TAN (conditional probability of each node given the
value of its parents) using ML criterion
When the dataset is small it is preferable to use the BD criterion to prevent the
overfitting of the model (Heckerman et al., 1995). The proposed ensemble acquires the
contribution from TAN classifier with ML test to predict the severity of the breast
masses.
