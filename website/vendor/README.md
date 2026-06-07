# Vendor Integrations

This folder contains custom integrations for **AstroWind**.

We are working to allow updates to template instances.
These are changes on the way to new **AstroWind v2**

---

## Frontend Design Plugin (Claude Code)

This project uses **Claude Code's `frontend-design` skill** for rapid, production-quality UI component development.

### What is it?

The `frontend-design` plugin is a specialized skill within Claude Code that generates distinctive, high-quality frontend interfaces without the generic aesthetics typical of AI-generated code.

### When to use it

Use the `frontend-design` skill when building:

- Custom UI components and widgets
- Landing pages and marketing sections
- Interactive interfaces and forms
- Design system components (buttons, cards, modals, etc.)

### How to invoke

```
/frontend-design
```

Or simply ask Claude:

- "Build a hero section with the frontend-design plugin"
- "Create a pricing table using frontend-design"
- "Design a contact form with the frontend-design skill"

### Benefits

- **Production-ready code**: Clean, maintainable, and follows best practices
- **Distinctive aesthetics**: Avoids generic AI design patterns
- **Fast iteration**: Quickly generate UI components that can be refined
- **Tailored to your stack**: Understands Astro, Tailwind CSS, and modern web frameworks

### Integration with AstroWind

The frontend-design plugin is particularly useful for:

- Creating custom page layouts beyond default AstroWind templates
- Building unique landing pages for specific campaigns or features
- Developing interactive components for case studies or portfolio items
- Rapid prototyping of new UI ideas before full implementation

---

## AstroWind Custom Integration

The `astrowind` folder contains the custom integration that loads `src/config.yaml` and provides configuration via a virtual module.
