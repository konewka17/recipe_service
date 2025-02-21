# 🍽️ Home Assistant Recipe Editor

This custom Home Assistant integration allows you to **view, edit, and add recipes** stored in a YAML file (`www/recipes.yaml`). It works with your **custom Lovelace card** to dynamically update recipes.

---

## 🚀 Features
- ✅ **Edit existing recipes** in `recipes.yaml`
- ✅ **Add new recipes** dynamically
- ✅ **Home Assistant service integration** (`recipes.update_recipe`)
- ✅ **Works with YAML-formatted recipes**
- ✅ **HACS-compatible** 🎉

---

## 💂️ Installation

### **1️⃣ Install via HACS**
1. Open **HACS → Integrations**.
2. Click the **three-dot menu** (top-right) → **Custom Repositories**.
3. Enter:
   ```
   https://github.com/yourusername/ha-recipes
   ```
4. Select **Integration** as the category.
5. Click **"Add"**, then find **Recipe Editor** in HACS and install it.
6. Restart Home Assistant.

### **2️⃣ Manual Installation**
1. Download the `recipes` folder.
2. Place it in `/config/custom_components/` (final path: `/config/custom_components/recipes/`).
3. Restart Home Assistant.

---

## 🔧 Setup
This integration **automatically registers a service** named `recipes.update_recipe`, which you can call from **Developer Tools → Services** or in automations.

Ensure your recipes file exists:  
📂 **Path:** `/config/www/recipes.yaml`  
📄 **Example File (`recipes.yaml`)**
```yaml
recipes:
  - id: pasta_bolognese
    name: Pasta Bolognese
    ingredients:
      - 250g pasta
      - 200g minced beef
      - 1 can tomato sauce
    instructions: Cook pasta, then add beef and sauce.
```

---

## 📌 Usage

### **📌 Update an Existing Recipe**
Use the `recipes.update_recipe` service to **modify a recipe**.

#### **Example YAML (Service Call)**
```yaml
service: recipes.update_recipe
data:
  recipe_id: pasta_bolognese
  new_yaml: |
    name: Pasta Bolognese
    ingredients:
      - 250g pasta
      - 200g minced beef
      - 1 can tomato sauce
      - 1 onion (chopped)
    instructions: Cook pasta, sauté onion, then add beef and sauce.
```

---

### **📌 Add a New Recipe**
If `recipe_id` does **not exist**, a **new recipe** is added.

#### **Example YAML (Service Call)**
```yaml
service: recipes.update_recipe
data:
  recipe_id: chicken_soup
  new_yaml: |
    name: Chicken Soup
    ingredients:
      - 1 whole chicken
      - 2 carrots
      - 1 onion
    instructions: Boil chicken with vegetables until tender.
```

---

## 🛠️ Advanced
### **Editing via UI**
If your **Lovelace card** supports editing, you can trigger this service dynamically when a user submits changes.

### **Automation Example**
Automatically add a recipe when a certain event occurs:
```yaml
alias: Add Chicken Soup Recipe on Trigger
trigger:
  - platform: event
    event_type: homeassistant_start
action:
  - service: recipes.update_recipe
    data:
      recipe_id: chicken_soup
      new_yaml: |
        name: Chicken Soup
        ingredients:
          - 1 whole chicken
          - 2 carrots
          - 1 onion
        instructions: Boil chicken with vegetables until tender.
```

---

## 📢 Contributing
Feel free to open an **issue or pull request** if you have improvements!

---

## 👤 Author
- **Your Name**
- GitHub: [@yourgithubusername](https://github.com/yourgithubusername)

---

## 📝 License
This project is licensed under the **MIT License**.

