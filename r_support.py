def install_r_packages(packages):
    # import rpy2's package module
    import rpy2.robjects.packages as rpackages
    # R vector of strings
    from rpy2.robjects.vectors import StrVector

    # import R's utility package
    utils = rpackages.importr('utils')

    # Selectively install what needs to be install.
    names_to_install = [x for x in packages if not rpackages.isinstalled(x)]

    if len(names_to_install) > 0:
        utils.install_packages(StrVector(names_to_install))
