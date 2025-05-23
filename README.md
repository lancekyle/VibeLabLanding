# The Vibe Lab - Landing Page

A minimalist, one-page landing site for TheVibeLab.ai newsletter and membership community. Designed for business and IT leaders in legacy enterprises who want to modernize with AI and automation.

## 🎨 Design Philosophy

The site features a unique "sticky note" aesthetic that represents the blend of traditional process planning and modern technology. Each section is designed as a colorful sticky note with handwritten-style typography, creating an approachable yet professional feel.

### Color Palette
- **Yellow**: #FFE24D (Hero section)
- **Purple**: #D9A1D8 (Newsletter signup)
- **Green**: #A2EA75 (Value proposition)
- **Orange**: #FFBB55 (Footer/contact)

## 🚀 Live Site

Visit the live site at: [thevibelab.ai](https://thevibelab.ai)

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Typography**: Caveat (handwritten style) + Open Sans (readability)
- **Icons**: Heroicons
- **Hosting**: Replit

## ✨ Features

- Responsive sticky note design
- Newsletter subscription with email validation
- Supabase integration for subscriber management
- Grid background pattern for authentic sticky note feel
- Mobile-optimized layout
- Success/error notifications for form submissions

## 🏃‍♂️ Running Locally

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `DATABASE_URL`: Your Supabase database connection string
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_ANON_KEY`: Your Supabase anonymous key

4. Run the application:
   ```bash
   python main.py
   ```

The app will be available at `http://localhost:5000`

## 📝 Database Setup

The application uses Supabase for storing newsletter subscriptions. The required table structure is automatically created when the app starts.

## 🎯 Target Audience

Business and IT leaders in legacy enterprises looking to:
- Modernize their operations with AI
- Learn about automation strategies
- Connect with a community of innovation-minded professionals

## 📧 Newsletter Integration

The site includes a seamless newsletter signup flow that:
- Validates email addresses
- Stores subscribers in Supabase
- Provides immediate feedback to users
- Prevents duplicate subscriptions

---

Built with ❤️ for enterprise innovators ready to embrace the future.