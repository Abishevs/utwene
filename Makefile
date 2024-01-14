SCRIPT_FILE = utwene.py
SCRIPT_NAME = utwene

INSTALL_DIR = $(HOME)/.local/bin

# 'make install' will run these commands
install:
	@chmod +x $(SCRIPT_FILE)
	@cp $(SCRIPT_FILE) $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "Script installed to $(INSTALL_DIR)/$(SCRIPT_NAME)"

# 'make uninstall' will remove the script from the install directory
uninstall:
	@rm -f $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "Script removed from $(INSTALL_DIR)/$(SCRIPT_NAME)"

