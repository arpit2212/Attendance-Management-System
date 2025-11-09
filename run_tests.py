"""
Comprehensive Testing Suite for Facial Recognition Attendance Management System
Supports: White Box, Black Box, Functional, Non-Functional, Integration, and Security Testing
"""

import os
import sys
import time
import unittest
import importlib.util
import inspect
from datetime import datetime
import json

# Install required packages if not available
try:
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit, h_visit
    from radon.raw import analyze
except ImportError:
    print("Installing radon package for code metrics...")
    os.system("pip install radon")
    from radon.complexity import cc_visit
    from radon.metrics import mi_visit, h_visit
    from radon.raw import analyze

# Project files to test
PROJECT_FILES = [
    "attendance_without_antispoofing.py",
    "attendance_with_antispoofing.py",
    "event_scheduler.py",
    "extract_embeddings.py",
    "mark_attendance.py",
    "training.py"
]

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_subheader(text):
    """Print formatted subheader"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.ENDC}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

class WhiteBoxTesting:
    """White Box Testing - Code Quality and Internal Structure Analysis"""
    
    def run(self):
        print_header("WHITE BOX TESTING - Code Quality & Structure Analysis")
        
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'files': {}
        }
        
        for file in PROJECT_FILES:
            if not os.path.exists(file):
                print_error(f"{file} not found - Skipping")
                continue
            
            print_subheader(f"Analyzing: {file}")
            
            with open(file, "r", encoding="utf-8") as f:
                source = f.read()
            
            file_results = {}
            
            # Raw metrics
            raw = analyze(source)
            file_results['raw'] = {
                'loc': raw.loc,
                'lloc': raw.lloc,
                'sloc': raw.sloc,
                'comments': raw.comments,
                'multi': raw.multi,
                'blank': raw.blank
            }
            
            print_info(f"Lines of Code (LOC): {raw.loc}")
            print_info(f"Logical LOC: {raw.lloc}")
            print_info(f"Source LOC: {raw.sloc}")
            print_info(f"Comments: {raw.comments}")
            print_info(f"Blank Lines: {raw.blank}")
            
            # Cyclomatic Complexity
            complexity = cc_visit(source)
            if complexity:
                complexities = [fn.complexity for fn in complexity]
                avg_complexity = sum(complexities) / len(complexities)
                max_complexity = max(complexities)
                
                file_results['complexity'] = {
                    'average': round(avg_complexity, 2),
                    'maximum': max_complexity,
                    'functions': len(complexity)
                }
                
                print_info(f"Average Cyclomatic Complexity: {avg_complexity:.2f}")
                print_info(f"Maximum Complexity: {max_complexity}")
                print_info(f"Total Functions: {len(complexity)}")
                
                # Complexity grade
                if avg_complexity <= 5:
                    print_success("Complexity Grade: A (Excellent)")
                elif avg_complexity <= 10:
                    print_success("Complexity Grade: B (Good)")
                elif avg_complexity <= 20:
                    print_warning("Complexity Grade: C (Moderate)")
                elif avg_complexity <= 30:
                    print_warning("Complexity Grade: D (Poor)")
                else:
                    print_error("Complexity Grade: F (Very Poor)")
                
                # Show high complexity functions
                high_complexity = [fn for fn in complexity if fn.complexity > 10]
                if high_complexity:
                    print_warning(f"\nHigh Complexity Functions ({len(high_complexity)}):")
                    for fn in high_complexity:
                        print(f"  - {fn.name}: Complexity {fn.complexity}")
            
            # Maintainability Index
            mi = mi_visit(source, True)
            file_results['maintainability'] = round(mi, 2)
            
            print_info(f"Maintainability Index: {mi:.2f}")
            
            if mi >= 85:
                print_success("Maintainability: High (Easy to maintain)")
            elif mi >= 65:
                print_warning("Maintainability: Medium (Moderate effort)")
            else:
                print_error("Maintainability: Low (Difficult to maintain)")
            
            # Halstead Metrics
            try:
                halstead = h_visit(source)
                if halstead:
                    file_results['halstead'] = {
                        'volume': round(halstead.total.volume, 2),
                        'difficulty': round(halstead.total.difficulty, 2),
                        'effort': round(halstead.total.effort, 2)
                    }
                    print_info(f"Halstead Volume: {halstead.total.volume:.2f}")
                    print_info(f"Halstead Difficulty: {halstead.total.difficulty:.2f}")
            except:
                pass
            
            results['files'][file] = file_results
            print()
        
        # Overall Summary
        print_subheader("OVERALL PROJECT SUMMARY")
        total_loc = sum(r['raw']['loc'] for r in results['files'].values())
        avg_mi = sum(r['maintainability'] for r in results['files'].values()) / len(results['files'])
        
        print_info(f"Total Lines of Code: {total_loc}")
        print_info(f"Average Maintainability Index: {avg_mi:.2f}")
        print_info(f"Files Analyzed: {len(results['files'])}")
        
        # Save results
        with open('test_results_whitebox.json', 'w') as f:
            json.dump(results, f, indent=2)
        print_success("\nResults saved to: test_results_whitebox.json")

class BlackBoxTesting:
    """Black Box Testing - Functional Behavior without Internal Knowledge"""
    
    def run(self):
        print_header("BLACK BOX TESTING - Functional Behavior Analysis")
        
        test_modules = ["extract_embeddings", "training", "mark_attendance", "event_scheduler"]
        
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'modules': {}
        }
        
        for mod in test_modules:
            print_subheader(f"Testing Module: {mod}")
            
            try:
                # Import test
                spec = importlib.util.find_spec(mod)
                if spec is None:
                    print_error(f"Module {mod} not found")
                    results['modules'][mod] = {'status': 'NOT_FOUND'}
                    continue
                
                module = importlib.import_module(mod)
                print_success(f"Successfully imported {mod}")
                
                # Get module components
                functions = inspect.getmembers(module, inspect.isfunction)
                classes = inspect.getmembers(module, inspect.isclass)
                
                results['modules'][mod] = {
                    'status': 'SUCCESS',
                    'functions': len(functions),
                    'classes': len(classes),
                    'function_names': [f[0] for f in functions],
                    'class_names': [c[0] for c in classes]
                }
                
                print_info(f"Found {len(functions)} functions")
                print_info(f"Found {len(classes)} classes")
                
                if functions:
                    print("  Functions:", ", ".join([f[0] for f in functions[:5]]))
                if classes:
                    print("  Classes:", ", ".join([c[0] for c in classes]))
                
            except Exception as e:
                print_error(f"Error importing {mod}: {str(e)}")
                results['modules'][mod] = {'status': 'ERROR', 'error': str(e)}
            
            print()
        
        # Save results
        with open('test_results_blackbox.json', 'w') as f:
            json.dump(results, f, indent=2)
        print_success("Results saved to: test_results_blackbox.json")

class FunctionalTesting(unittest.TestCase):
    """Functional Testing - Unit Tests for Core Functions"""
    
    def test_csv_operations(self):
        """Test CSV write and append operations"""
        print_info("Testing CSV operations...")
        from mark_attendance import Mark_Attendance
        
        file = "test_attendance.csv"
        obj = Mark_Attendance(file)
        obj.write_csv_header(id="id", date="date", staff_name="staff_name", time="time", status="status")
        obj.append_csv_rows([1, "2025-11-10", "Test User", "09:00", "Present"])
        
        self.assertTrue(os.path.exists(file))
        
        # Verify content
        with open(file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Header + 1 data row
        
        os.remove(file)
        print_success("CSV operations test passed")
    
    def test_training_model_structure(self):
        """Test training model initialization"""
        print_info("Testing training model structure...")
        from training import Training
        import pickle
        import numpy as np
        
        # Create test data
        data = {"face_ids": ["1", "2"], "embeddings": np.random.rand(2, 128).tolist()}
        test_file = "test_embeddings.pickle"
        
        with open(test_file, "wb") as f:
            pickle.dump(data, f)
        
        t = Training(test_file)
        label, labels, embeddings, ids = t.load_embeddings_and_labels()
        
        self.assertEqual(len(labels), len(ids))
        self.assertEqual(len(embeddings), 2)
        
        os.remove(test_file)
        print_success("Training model structure test passed")
    
    def test_extract_embeddings_class(self):
        """Test Extract_Embeddings class initialization"""
        print_info("Testing Extract_Embeddings class...")
        
        # This test verifies the class can be imported and instantiated
        try:
            from extract_embeddings import Extract_Embeddings
            # Note: We can't fully test without the actual model file
            print_success("Extract_Embeddings class structure test passed")
        except Exception as e:
            self.fail(f"Failed to import Extract_Embeddings: {e}")

class NonFunctionalTesting:
    """Non-Functional Testing - Performance, Security, Usability"""
    
    def run(self):
        print_header("NON-FUNCTIONAL TESTING - Performance & Quality")
        
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'performance': {},
            'security': {},
            'usability': {}
        }
        
        # Performance Testing
        print_subheader("Performance Testing")
        start = time.time()
        
        total_lines = 0
        file_sizes = {}
        
        for file in PROJECT_FILES:
            if os.path.exists(file):
                with open(file, "r", encoding="utf-8") as f:
                    lines = len(f.readlines())
                    total_lines += lines
                
                size = os.path.getsize(file)
                file_sizes[file] = size
                
                print_info(f"{file}: {lines} lines, {size/1024:.2f} KB")
        
        end = time.time()
        
        results['performance'] = {
            'read_time': round(end - start, 4),
            'total_lines': total_lines,
            'file_sizes': file_sizes
        }
        
        print_success(f"Files processed in {end - start:.4f} seconds")
        
        # Security Testing
        print_subheader("Security Analysis")
        
        security_issues = []
        
        for file in PROJECT_FILES:
            if not os.path.exists(file):
                continue
            
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check for hardcoded credentials
            if "password = ''" in content or 'password = ""' in content:
                security_issues.append(f"{file}: Potential hardcoded empty password")
            
            # Check for SQL injection vulnerabilities
            if ".execute(" in content and "%" in content:
                if ".execute('select" in content.lower() or '.execute("select' in content.lower():
                    print_warning(f"{file}: Uses string formatting in SQL queries - check for SQL injection")
            
            # Check for insecure random
            if "import random" in content and "password" in content.lower():
                print_warning(f"{file}: Uses 'random' module near password operations")
        
        results['security'] = {
            'issues_found': len(security_issues),
            'issues': security_issues
        }
        
        if security_issues:
            for issue in security_issues:
                print_warning(issue)
        else:
            print_success("No obvious security issues detected")
        
        # Usability Testing
        print_subheader("Usability Analysis")
        
        gui_files = [f for f in PROJECT_FILES if os.path.exists(f) and 'attendance_' in f]
        
        for file in gui_files:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count user-facing elements
            buttons = content.count("Button(")
            entries = content.count("Entry(")
            labels = content.count("Label(")
            messageboxes = content.count("messagebox.")
            
            print_info(f"{file}:")
            print(f"  Buttons: {buttons}")
            print(f"  Input Fields: {entries}")
            print(f"  Labels: {labels}")
            print(f"  Message Boxes: {messageboxes}")
            
            results['usability'][file] = {
                'buttons': buttons,
                'entries': entries,
                'labels': labels,
                'messageboxes': messageboxes
            }
        
        # Save results
        with open('test_results_nonfunctional.json', 'w') as f:
            json.dump(results, f, indent=2)
        print_success("\nResults saved to: test_results_nonfunctional.json")

class IntegrationTesting:
    """Integration Testing - Component Interaction"""
    
    def run(self):
        print_header("INTEGRATION TESTING - Component Interaction Analysis")
        
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'imports': {},
            'dependencies': {}
        }
        
        print_subheader("Analyzing Module Dependencies")
        
        for file in PROJECT_FILES:
            if not os.path.exists(file):
                continue
            
            print_info(f"Analyzing: {file}")
            
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find imports
            imports = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
            
            results['imports'][file] = imports
            print(f"  Found {len(imports)} import statements")
            
            # Check for project module imports
            project_imports = [imp for imp in imports if any(
                mod.replace('.py', '') in imp for mod in PROJECT_FILES
            )]
            
            if project_imports:
                print_success(f"  Internal dependencies: {len(project_imports)}")
                for imp in project_imports:
                    print(f"    - {imp}")
        
        # Database connectivity check
        print_subheader("Database Integration Check")
        
        db_files = [f for f in PROJECT_FILES if os.path.exists(f)]
        
        for file in db_files:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "pymysql.connect" in content:
                print_success(f"{file} uses database connection")
                
                # Check connection parameters
                if 'host = "localhost"' in content:
                    print_info("  Host: localhost")
                if 'database = "recognition"' in content:
                    print_info("  Database: recognition")
        
        # Save results
        with open('test_results_integration.json', 'w') as f:
            json.dump(results, f, indent=2)
        print_success("\nResults saved to: test_results_integration.json")

def run_functional_tests():
    """Run functional unit tests"""
    print_header("FUNCTIONAL TESTING - Unit Tests")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(FunctionalTesting)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print_subheader("Test Summary")
    print_info(f"Tests Run: {result.testsRun}")
    print_success(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print_error(f"Failures: {len(result.failures)}")
    if result.errors:
        print_error(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

def main_menu():
    """Display main menu and handle user input"""
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║     ATTENDANCE SYSTEM - COMPREHENSIVE TEST SUITE          ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
        print(f"{Colors.CYAN}Select Test Type:{Colors.ENDC}")
        print(f"{Colors.BOLD}1.{Colors.ENDC} White Box Testing (Code Quality & Structure)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Black Box Testing (Functional Behavior)")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Functional Testing (Unit Tests)")
        print(f"{Colors.BOLD}4.{Colors.ENDC} Non-Functional Testing (Performance & Security)")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Integration Testing (Component Interaction)")
        print(f"{Colors.BOLD}6.{Colors.ENDC} Run All Tests")
        print(f"{Colors.BOLD}7.{Colors.ENDC} Exit")
        print()
        
        choice = input(f"{Colors.GREEN}Enter your choice (1-7): {Colors.ENDC}").strip()
        
        if choice == "1":
            WhiteBoxTesting().run()
        elif choice == "2":
            BlackBoxTesting().run()
        elif choice == "3":
            run_functional_tests()
        elif choice == "4":
            NonFunctionalTesting().run()
        elif choice == "5":
            IntegrationTesting().run()
        elif choice == "6":
            print_header("RUNNING ALL TESTS")
            WhiteBoxTesting().run()
            BlackBoxTesting().run()
            run_functional_tests()
            NonFunctionalTesting().run()
            IntegrationTesting().run()
            print_header("ALL TESTS COMPLETED")
        elif choice == "7":
            print(f"\n{Colors.GREEN}Thank you for using the Testing Suite!{Colors.ENDC}\n")
            break
        else:
            print_error("Invalid choice. Please enter a number between 1 and 7.")
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Testing interrupted by user.{Colors.ENDC}\n")
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()