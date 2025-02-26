import subprocess
from xml.dom import minidom
import os



class CommandManualGenerator(): #to read commands from the file
    def __init__(self,file):
        self.file=file
    def generate_manual(self):
        self.file = open(f"{self.file}", "r")
        self.content = self.file.read()
        self.command_list = self.content.split("\n")
        return self.command_list
       

class CommandManual(): #to generate each command manual
    def __init__(self, command):
        self.command = command
     
    def generate_description(self, command): #getting the description
        des = f"man {command} | awk '/^DESCRIPTION/,/^$/' | grep -v '^$' | sed '1d' | cut -c 8- | tr -s ' '"
        description = subprocess.run(des, shell=True, capture_output=True, text=True)
        return description.stdout.strip()

    def generate_version(self, command): #getting the version
        ver = f"{command} --version | sed -n '1p' | tr -s ' ' | tr '\n' ' '"
        version = subprocess.run(ver, shell=True, capture_output=True, text=True)
        return version.stdout.strip()

    def generate_related_commands(self, command): #get some related commands :)
        if command == "chmod":
            related_comm = f"bash -c 'compgen -c | grep ^ch | head -n 5'"
        elif command == "rm":
            related_comm = f"bash -c 'compgen -c | grep ^rm | head -n 5'"
        elif command == "head":
            related_comm = f"bash -c 'compgen -c | grep he| head -n 5'"
        elif command == "apropos":
            related_comm = f"bash -c 'compgen -c | grep pos| head -n 5'"
        elif command == "uname":
            related_comm = f"bash -c 'compgen -c | grep name | head -n 5'"
        elif command == "sed":
            related_comm = f"bash -c 'compgen -c |  grep se[a-z] | head -n 5'"
        else:
            related_comm = f"bash -c 'compgen -c | grep {command} | head -n 5 '"
        
        related = subprocess.run(related_comm, shell=True, capture_output=True, text=True)
        return related.stdout.strip()

    def generate_example(self, command): #get examples
        example = ""
        if command == "cat":
            example = "cat file.txt"
        elif command == "chmod":
            example = "chmod 777 file.txt"
        elif command == "wc":
            example = "cat file.txt | wc -l "
        elif command == "tr":
            example = "cat file.txt | tr [a-z] [A-Z]"
        elif command == "cut":
            example = "cat file.txt | cut -c1-10"
        elif command == "head":
            example = "head -n 3 file.txt | cut -c1-10"
        elif command == "tail":
            example = "tail -n 3 file.txt | cut -c1-10"
        elif command == "ls":
            example = "ls -l file.txt | cut -c1-10"
        elif command == "apropos":
            example = "apropos '^list' | sed -n '1p'"
        elif command == "cmp":
            example = "cmp test_file test_file2"
        elif command == "cp":
            example = "cp test_file test_file2"
        elif command == "rm":
            example = "rm test_file"
        elif command == "sed":
            example = "sed 's/linux/LINUX/g' test_file"
        else:
            example = command
        return example
    
    def generate_syntax(self, command): #to add common syntax for the the manual
     syntax = ""
     if command == "cat":
        syntax = "cat [options] [file(s)]"
     elif command == "chmod":
        syntax = "chmod [options] mode file(s)"
     elif command == "wc":
        syntax = "wc [options] [file(s)]"
     elif command == "tr":
        syntax = "tr [options] set1 set2"
     elif command == "sed":
        syntax = "sed [options] script [file(s)]"
     elif command == "who":
        syntax = "who [options]"
     elif command == "cut":
        syntax = "cut [options] [file(s)]"
     elif command == "date":
        syntax = "date [options]"
     elif command == "ls":
        syntax = "ls [options] [file(s)]"
     elif command == "rm":
        syntax = "rm [options] [file(s)]"
     elif command == "cp":
        syntax = "cp [options] source destination"
     elif command == "head":
        syntax = "head [options] [file(s)]"
     elif command == "tail":
        syntax = "tail [options] [file(s)]"
     elif command == "sort":
        syntax = "sort [options] [file(s)]"
     elif command == "apropos":
        syntax = "apropos [options] keyword(s)"
     elif command == "arch":
        syntax = "arch [options]"
     elif command == "id":
        syntax = "id [options] [username]"
     elif command == "uname":
        syntax = "uname [options]"
     elif command == "free":
        syntax = "free [options]"
     elif command == "cmp":
        syntax = "cmp [options] file1 file2 [skip1 [skip2]]"
    
     return syntax.strip()
    
    def generate_usage_pattern(self, command): #this part is added to manual to show what the command is uesd for
     usage = ""
     if command == "cat":
        usage = "Concatenate and display the content of one or more files."
     elif command == "chmod":
        usage = "Change the permissions of a file or directory."
     elif command == "wc":
        usage = "Count the number of lines, words, and bytes in files."
     elif command == "tr":
        usage = "Translate or delete characters from standard input, writing to standard output."
     elif command == "sed":
        usage = "Stream editor for filtering and transforming text."
     elif command == "who":
        usage = "Show who is logged on."
     elif command == "cut":
        usage = "Remove sections from each line of files."
     elif command == "date":
        usage = "Display or set the system date and time."
     elif command == "ls":
        usage = "List directory contents."
     elif command == "rm":
        usage = "Remove files or directories."
     elif command == "cp":
        usage = "Copy files and directories."
     elif command == "head":
        usage = "Output the first part of files."
     elif command == "tail":
        usage = "Output the last part of files."
     elif command == "sort":
        usage = "Sort lines of text files."
     elif command == "apropos":
        usage = "Search the manual page names and descriptions for a regular expression."
     elif command == "arch":
        usage = "Display machine architecture."
     elif command == "id":
        usage = "Print user and group information for the specified username."
     elif command == "uname":
        usage = "Print system information."
     elif command == "free":
        usage = "Display amount of free and used memory in the system."
     elif command == "cmp":
        usage = "Compare two files byte by byte."
    
     return usage.strip()
    
    def generate_doc_link(self, command):# online documintation links to the list of commands
    
     doc_link = f"https://man7.org/linux/man-pages/man1/{command}.1.html"
    
     return doc_link.strip()



        


    

class XmlSerializer(): #creating the xml file for choosen command
    def __init__(self,command):
     self.command=command
    def generate_xml(self,command):
            manual= CommandManual(command)
            description = manual.generate_description(command)
            version = manual.generate_version(command)
            related_commands = manual.generate_related_commands(command)
            example = manual.generate_example(command)
            syntax =manual.generate_syntax(command)
            usage=manual.generate_usage_pattern(command)
            doc_link=manual.generate_doc_link(command)
            
            

            root = minidom.Document()
            manuals = root.createElement('Manuals')
            root.appendChild(manuals)

            command_manual = root.createElement('CommandManual')
            manuals.appendChild(command_manual)

            command_name = root.createElement('CommandName')
            command_name.appendChild(root.createTextNode(command))
            command_manual.appendChild(command_name)

            command_description = root.createElement('CommandDescription')
            command_description.appendChild(root.createTextNode(description))
            command_manual.appendChild(command_description)

            version_history = root.createElement('VersionHistory')
            version_history.appendChild(root.createTextNode(version))
            command_manual.appendChild(version_history)

            example_element = root.createElement('Example')
            example_element.appendChild(root.createTextNode(example))
            command_manual.appendChild(example_element)

            related_commands_element = root.createElement('RelatedCommands')
            related_commands_element.appendChild(root.createTextNode(related_commands))
            command_manual.appendChild(related_commands_element)

            syntax_element = root.createElement('syntax')
            syntax_element.appendChild(root.createTextNode(syntax))
            command_manual.appendChild(syntax_element)

            usage_pattern_element = root.createElement('UsagePatterns')
            usage_pattern_element.appendChild(root.createTextNode(usage))
            command_manual.appendChild(usage_pattern_element)

            OnlineDocumentationLink_element = root.createElement('OnlineDocumentationLink')
            OnlineDocumentationLink_element.appendChild(root.createTextNode(doc_link))
            command_manual.appendChild(OnlineDocumentationLink_element)

            

            save_path_file = f"{command}_manual.xml"

            with open(save_path_file, "w") as f:
                f.write(root.toprettyxml(indent="\t"))
        
    

class CommandManualVerifier(): #to verify command
    def __init__(self):
        pass

    def verify_manual(self, command):
        manual_file = f"{command}_manual.xml"

        if not os.path.exists(manual_file):
            print(f"Manual file for command '{command}' does not exist.")
            return

        with open(manual_file, "r") as f:
            content = f.read()

        # Parse XML content
        try:
            xml_content = minidom.parseString(content)
        except Exception as e:
            print(f"Error parsing XML for command '{command}': {str(e)}")
            return
        
        des = f"man {command} | awk '/^DESCRIPTION/,/^$/' | grep -v '^$' | sed '1d' | cut -c 8- | tr -s ' '"
        description = subprocess.run(des, shell=True, capture_output=True, text=True)

        ver = f"{command} --version | sed -n '1p' | tr -s ' ' | tr '\n' ' '"
        version = subprocess.run(ver, shell=True, capture_output=True, text=True)


        if command == "chmod":
            related_comm = f"bash -c 'compgen -c | grep ^ch | head -n 5'"
        elif command == "rm":
            related_comm = f"bash -c 'compgen -c | grep ^rm | head -n 5'"
        elif command == "head":
            related_comm = f"bash -c 'compgen -c | grep he| head -n 5'"
        elif command == "apropos":
            related_comm = f"bash -c 'compgen -c | grep pos| head -n 5'"
        elif command == "uname":
            related_comm = f"bash -c 'compgen -c | grep name | head -n 5'"
        elif command == "sed":
            related_comm = f"bash -c 'compgen -c |  grep se[a-z] | head -n 5'"
        else:
            related_comm = f"bash -c 'compgen -c | grep {command} | head -n 5 '"
        
        related = subprocess.run(related_comm, shell=True, capture_output=True, text=True)
        
        

        command_name = xml_content.getElementsByTagName('CommandName')[0].firstChild.data.strip()
        
        command_description = xml_content.getElementsByTagName('CommandDescription')[0].firstChild.data.strip()
        
        version_history = xml_content.getElementsByTagName('VersionHistory')[0].firstChild.data.strip()

        example = xml_content.getElementsByTagName('Example')[0].firstChild.data.strip()

        related_commands = xml_content.getElementsByTagName('RelatedCommands')[0].firstChild.data.strip()
        

        # Compare with original content
    

        changes = []
        if command_name != command:
           changes.append(f"Name for command '{command}' has changed.")
        if command_description != description.stdout.strip(): 
            changes.append(f"Description for command '{command}' has changed.")
        if version_history != version.stdout.strip():
            changes.append(f"Example for command '{command}' has changed.")
        if related_commands != related.stdout.strip():
            changes.append(f"related commands for command '{command}' has changed.")


        

        if not changes:
            print(f"Manual content for command '{command}' is correct.")
        else:
            print(f"Changes detected for command '{command}':")
            for change in changes:
                print(change)

class search_Manual(): #search for / in file
    def __init__(self):
        pass

    def search_function(self, command, section):
        manual_file = f"{command}_manual.xml"

        if not os.path.exists(manual_file):
            print(f"Manual file for command '{command}' does not exist.")
            return

        with open(manual_file, "r") as f:
            content = f.read()

        # Parse XML content
        try:
            xml_content = minidom.parseString(content)
        except Exception as e:
            print(f"Error parsing XML for command '{command}': {str(e)}")
            return
        
        print("Command Manual exists !\n")
        print("here is search results:")

        if section == "description":
            command_description = xml_content.getElementsByTagName('CommandDescription')[0].firstChild.data.strip()
            print(command_description)
        elif section == "version":
            version_history = xml_content.getElementsByTagName('VersionHistory')[0].firstChild.data.strip()
            print(version_history)
        elif section == "example":
            example = xml_content.getElementsByTagName('Example')[0].firstChild.data.strip()
            print(example)
        elif section == "related_commands":
            related_commands = xml_content.getElementsByTagName('RelatedCommands')[0].firstChild.data.strip()
            print(related_commands)
        
        elif section == "UsagePatterns":
            UsagePatterns = xml_content.getElementsByTagName('UsagePatterns')[0].firstChild.data.strip()
            print(UsagePatterns)

        elif section == "syntax":
            syntax = xml_content.getElementsByTagName('syntax')[0].firstChild.data.strip()
            print(syntax)

        elif section == "OnlineDocumentationLink":
            OnlineDocumentationLink = xml_content.getElementsByTagName('OnlineDocumentationLink')[0].firstChild.data.strip()
            print(OnlineDocumentationLink)


class Recommendation_system():
    def __init__(self):
        pass

    def Recommendation_function(self, command):
        if command=="cat":
            print("1. tac")
            print("2. less")
            print("3. more")
        elif command == "chmod":
            print("1. chown")
            print("2. chgrp")
        elif command == "wc":
            print("1. sed")
            print("2. awk")
        elif command =="tr":
            print("1. sed")
            print("2. perl")
        elif(command == "who"):
            print("1. users")
            print("2. whoami")
            print("3. id")
            print("4. w")
        elif(command == "cut"):
            print("1. sed")
            print("2. paste")
            print("3. awk")

        elif(command == "date"):
            print("1. cal")
            print("2. uptime")

        elif(command == "rm"):
            print("1. rmdir")
            print("2. unlink")
            print("3. trash-put")
        
        elif(command == "cp"):
            print("1. rsync")
            print("2. tar")
        
        elif(command == "head"):
            print("1. cat")
            print("2. tail")

        elif(command == "tail"):
            print("1. cat")
            print("2. head")
        elif(command == "sort"):
            print("1. uniq")
            print("2. awk")
        elif(command == "arch"):
            print("1. uname")
            print("2. lscpu")
            print("3. inxi")
        elif (command == "apropos"):
            print("1. man")
            print("2. whatis")
        elif (command == "id"):
            print("1. groups")
            print("2. whoami")
        elif (command == "uname"):
            print("1. arch")
            print("2. hostname")
        elif (command == "free"):
            print("1. top")
            print("2. vmstat")
        elif (command == "cmp"):
            print("1. diff")
            print("2. sdiff")



# Usage
generator = CommandManualGenerator("commands.txt")
list=generator.generate_manual()
print("This is commands list:")
for item in range (20):
  print(list[item])

for item in range (20):
    manual_creaation = CommandManual(list[item])
    xml_create=XmlSerializer(list[item])
    xml_create.generate_xml(list[item])


print("finished generating Manuals ! ")
# Usage
print("do you want to verify any command? yes/no")
answer=input()
if answer== "yes":
 verifier = CommandManualVerifier()
 print("Enter command you want to verify")
 command =input()
 verifier.verify_manual(command)

print("do you want to serch for any command? yes/no")
answer=input()
if answer== "yes":
 search = search_Manual()
 print("Enter command you want to search for")
 command =input()
 print("Enter what section you want to see (enter a number)")
 print("1.description")
 print("2.example")
 print("3.version")
 print("4.related commands")
 print("5.Usage Patterns")
 print("6.syntax")
 print("7.Online Documentation Link")
 choice =int(input())
 
 if choice ==1:
  search.search_function(command,"description")
 elif choice == 2:
  search.search_function(command,"example")
 elif choice ==3:
  search.search_function(command,"version")
 elif choice == 4: 
  search.search_function(command,"related_commands")
 elif choice ==5:
  search.search_function(command,"UsagePatterns")
 elif choice ==6:
  search.search_function(command,"syntax")
 elif choice ==7:
  search.search_function(command,"OnlineDocumentationLink")


 print("\n-------Recommendation-------")
 print(f"you recently searched for {command} ")
 print("you can see this also: ")
 recommenting=Recommendation_system()
 recommenting.Recommendation_function(command)
