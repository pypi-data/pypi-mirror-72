from ..Utils.executeRest import execute
import logging
import json
from ..Utils.incapError import IncapError
from ..Accounts.account_audit import Audit


def r_audit(args):
    output = 'Get account audit events.'
    logging.basicConfig(format='%(levelname)s - %(message)s',  level=getattr(logging, args.log.upper()))
    print(output)
    param = vars(args)

    result = read(param)

    if int(result.get('res')) != 0:
        err = IncapError(result)
        err.log()
    elif 'audit_events' in result:
        print('Account audit events following:\n')
        for events in result.get('audit_events'):
            audit = Audit(events)
            print(audit.log())


def read(params):
    resturl = 'accounts/audit'

    if params:
        if "account_id" in params:
            return execute(resturl, params)
        else:
            logging.warning("No account_id parameter has been passed in for %s." % __name__)
    else:
        logging.error('No parameters where passed in.')
