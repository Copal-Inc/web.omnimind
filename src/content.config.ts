import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({ // Aqui se colocan los campos que queremos que tenga cada articulo - Importante para Decap

			// (consultarlo con OMNIMIND para conocer la estructura de sus blogs)
			title: z.string(),
			description: z.string(),
			// Fechas (soporta publishDate y pubDate para mantener compatibilidad)
			publishDate: z.coerce.date().optional(),
			pubDate: z.coerce.date().optional(),
			updatedDate: z.coerce.date().optional(),

			// Metadatos de autoría y categorización
			author: z.string().optional(),
			category: z.string().optional(),
			tags: z.array(z.string()).default([]),

			// Portada / Imágenes
			cover: z.string().optional(),
			coverAlt: z.string().optional(),
			heroImage: z.optional(image()),

			// Estado y visibilidad del post
			draft: z.boolean().default(false),
			featured: z.boolean().default(false),
		}),
});

export const collections = { blog };
