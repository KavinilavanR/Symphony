import { rest } from 'msw';

export const handlers = [
	rest.get('/api/qna', (req, res, ctx) => {
		return res(
			ctx.delay(2000),
			ctx.status(200),
			ctx.json({
				answer: [
					{
						id: '283',
						title: 'Pediatric Oncology',
						abstract:
							'Oral Abstract Session	Impact of asparaginase discontinuation on outcome in childhood ALL: A report from the Children’s Oncology Group (COG).',
					},
					{
						id: '1005',
						title: 'Red Cells and Erythropoiesis, Excluding Iron',
						abstract:
							'Oral Session	Dysplastic Erythropoiesis in Stag2 Loss Exhibits Defective Nuclear Condensation and Hemophagocytosis',
					},
				],
			})
		);
	}),
];
