import asyncio
import os
import sys
import importlib
sys.dont_write_bytecode = True
import modules.utils.palog as log

###################################################################################################
# ██████   ██████      ███    ██  ██████  ████████     ████████  ██████  ██    ██  ██████ ██   ██ #
# ██   ██ ██    ██     ████   ██ ██    ██    ██           ██    ██    ██ ██    ██ ██      ██   ██ #
# ██   ██ ██    ██     ██ ██  ██ ██    ██    ██           ██    ██    ██ ██    ██ ██      ███████ #
# ██   ██ ██    ██     ██  ██ ██ ██    ██    ██           ██    ██    ██ ██    ██ ██      ██   ██ #
# ██████   ██████      ██   ████  ██████     ██           ██     ██████   ██████   ██████ ██   ██ #
#-------------------------------------------------------------------------------------------------#
#                 Do not modify this file. No support will be provided if modified.               #
###################################################################################################           

async def module_loader():
    modules = [f[:-3] for f in os.listdir('modules') if f.endswith('.py') and f != '__init__.py']
    if not modules:
        log.critical('[MAIN LOADER] No modules found in modules directory. Exiting.')
        return
    tasks = []
    for module in modules:
        try:
            module_file = f'modules/{module}.py'
            if os.path.isfile(module_file):
                module = importlib.import_module(f'modules.{module}')
                if hasattr(module, 'run') and asyncio.iscoroutinefunction(module.run):
                    tasks.append(asyncio.create_task(module.run()))
                else:
                    log.warning(f'[MAIN LOADER] Module {module_file} has no run function. Skipping.')
            else:
                log.error(f'[MAIN LOADER] No file found for module {module_file}. Skipping.')
        except ImportError:
            log.error(f'[MAIN LOADER] Failed to import module {module}\n{sys.exc_info()}')

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        log.info('[MAIN LOADER] Closing all modules safely.')

async def main():
    try:
        await module_loader()
    except KeyboardInterrupt:
        log.info('[MAIN LOADER] Keyboard interrupt. Exiting.')
    except Exception as e:
        log.error(f'[MAIN LOADER] An error occurred during module loading.\n{e}')

asyncio.run(main())