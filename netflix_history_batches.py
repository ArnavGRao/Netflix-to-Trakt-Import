import csv
import logging

from NetflixTvShow import NetflixTvHistory


NETFLIX_HISTORY_BATCH_SIZE = 250


def getNetflixHistoryBatches(inputFile, inputFileDelimiter, batchSize):
    """
    Parses Netflix viewing history in CSV format and yields it in batches.

    :param inputFile: File containing Netflix viewing history
    :param inputFileDelimiter: Delimiter used in Netflix viewing history (ex. CSV = `,`)
    :param batchSize: Number of entries to include in each batch
    :return: Yields `netflixHistory` objects containing parsed viewing history CSV batches
    """
    with open(inputFile, mode="r", encoding="utf-8") as csvFile:
        csvReader = csv.DictReader(
            csvFile, fieldnames=("Title", "Date"), delimiter=inputFileDelimiter
        )
        line_count = 0
        batch_entry_count = 0
        netflixHistory = NetflixTvHistory()

        for row in csvReader:
            if line_count == 0:
                line_count += 1
                continue

            entry = row["Title"]
            watchedAt = row["Date"]

            logging.debug("Parsed CSV file entry: {} : {}".format(watchedAt, entry))

            netflixHistory.addEntry(entry, watchedAt)
            batch_entry_count += 1
            line_count += 1

            if batch_entry_count >= batchSize:
                logging.info(f"Processed {batch_entry_count} entries in current batch.")
                yield netflixHistory
                netflixHistory = NetflixTvHistory()
                batch_entry_count = 0

        logging.info(f"Processed {line_count} lines.")

        if batch_entry_count > 0:
            yield netflixHistory
