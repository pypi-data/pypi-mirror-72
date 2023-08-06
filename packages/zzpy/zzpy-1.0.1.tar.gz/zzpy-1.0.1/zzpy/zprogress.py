def pb(iterable, total=None, title='进度', min_interval=10, max_interval=60, ncols=80):
    if not total:
        try:
            total = len(iterable)
        except Exception as ex:
            pass
        
    from tqdm import tqdm
    return tqdm(iterable,
                total=total,
                desc=f'\n{title}',
                mininterval=min_interval,
                maxinterval=max_interval,
                ncols=ncols)


def main():
    import time
    for i in pb(range(500), title='任务'):
        time.sleep(0.02)


if __name__ == "__main__":
    main()
