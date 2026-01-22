from radish import after
import os

# Number of retries (default = 1)
MAX_RETRIES = int(os.getenv("RADISH_RETRIES", "1"))

@after.each_scenario
def retry_failed_scenario(scenario):
    if not scenario.failed:
        return

    # Track retries on scenario context
    retries = getattr(scenario.context, "retries", 0)

    if retries < MAX_RETRIES:
        scenario.context.retries = retries + 1

        # Mark scenario to be re-executed
        scenario.state = scenario.State.UNTESTED

#export RADISH_RETRIES=2