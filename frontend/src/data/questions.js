export const QUESTIONS = [
  {
    id: "age",
    label: "Your age",
    options: [
      { value: "under_18", label: "Under 18" },
      { value: "18-24", label: "18–24" },
      { value: "25-34", label: "25–34" },
      { value: "35-44", label: "35–44" },
      { value: "45_plus", label: "45+" },
    ],
  },
  {
    id: "gender",
    label: "Gender",
    options: [
      { value: "male", label: "Male" },
      { value: "female", label: "Female" },
      { value: "na", label: "Prefer not to say" },
    ],
  },
  {
    id: "frequency",
    label: "How often do you buy chocolate?",
    options: [
      { value: "daily", label: "Almost every day" },
      { value: "weekly", label: "A few times a week" },
      { value: "monthly", label: "A few times a month" },
      { value: "rarely", label: "Rarely" },
    ],
  },
  {
    id: "priority",
    label: "What matters most when choosing chocolate?",
    options: [
      { value: "price", label: "Price" },
      { value: "brand", label: "Brand" },
      { value: "taste", label: "Taste" },
      { value: "discount", label: "Deals & discounts" },
      { value: "rating", label: "Reviews & rating" },
    ],
  },
  {
    id: "discount_driven",
    label: "Do discounts drive your purchase?",
    options: [
      { value: "always", label: "Yes, almost always" },
      { value: "sometimes", label: "Sometimes" },
      { value: "no", label: "No, I look at the product itself" },
    ],
  },
];
