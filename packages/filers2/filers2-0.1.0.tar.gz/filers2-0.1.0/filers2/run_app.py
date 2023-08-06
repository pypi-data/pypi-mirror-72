
if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    from filers2.main import run_app
    run_app()
