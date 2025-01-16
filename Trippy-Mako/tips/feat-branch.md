### **Step 1: Create a New Feature Branch**
1. **Ensure You Are on the `main` Branch:**
   ```bash
   git checkout main
   ```
2. **Pull the Latest Changes (Optional but Recommended):**
   ```bash
   git pull origin main
   ```
3. **Create a New Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

### **Step 2: Work on the Feature**
1. Make the necessary code changes in your local repository.
2. Stage your changes:
   ```bash
   git add .
   ```
3. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add a brief description of your changes"
   ```

---

### **Step 3: Push the Feature Branch**
1. Push your branch to the remote repository:
   ```bash
   git push origin feature/your-feature-name
   ```

---

### **Step 4: Merge the Feature Branch into `main`**
1. **Switch to the `main` Branch:**
   ```bash
   git checkout main
   ```
2. **Pull the Latest Changes on `main`:**
   ```bash
   git pull origin main
   ```
3. **Merge the Feature Branch:**
   ```bash
   git merge feature/your-feature-name
   ```
4. **Resolve Any Merge Conflicts (if applicable):**
   - Open the conflicting files and make necessary changes.
   - Stage the resolved files:
     ```bash
     git add <file>
     ```
   - Complete the merge:
     ```bash
     git commit
     ```

---

### **Step 5: Clean Up**
1. **Delete the Feature Branch Locally:**
   ```bash
   git branch -d feature/your-feature-name
   ```
2. **Delete the Feature Branch from the Remote Repository:**
   ```bash
   git push origin --delete feature/your-feature-name
   ```

---

### **Step 6: Push the Updated `main` Branch**
1. Push your updated `main` branch to the remote repository:
   ```bash
   git push origin main
   ```

--- 
