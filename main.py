import asyncio
import os
import sys
import importlib
import aiohttp
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

async def autoupdate():
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get('https://api.github.com/repos/ItzPabz/paBots-Autoloader/contents/')
            if response.status == 200:
                files = await response.json()
                for file in files:
                    if file['type'] == 'file':
                        file_name = file['name']
                        file_url = file['download_url']
                        response = await session.get(file_url)
                        if response.status == 200:
                            content = await response.text()
                            if not os.path.isfile(file_name) or content != open(file_name, 'r', encoding='utf-8').read():
                                with open(file_name, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                log.debug(f'[AUTOUPDATE] Updated {file_name} successfully.')
                            else:
                                log.debug(f'[AUTOUPDATE] {file_name} is up to date.')
                        else:
                            log.error(f'[AUTOUPDATE] Failed to update {file_name}. Status code: {response.status}')
            else:
                log.error(f'[AUTOUPDATE] Failed to retrieve repository contents. Status code: {response.status}')
    except Exception as e:
        log.error(f'[AUTOUPDATE] An error occurred during autoupdate.\n{e}')

async def main():
    try:
        await autoupdate()
        await module_loader()
    except KeyboardInterrupt:
        log.info('[MAIN LOADER] Keyboard interrupt. Exiting.')
    except Exception as e:
        log.error(f'[MAIN LOADER] An error occurred during module loading.\n{e}')

asyncio.run(main())
