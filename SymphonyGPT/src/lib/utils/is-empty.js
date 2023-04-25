export default function isEmpty(value) {
	try {
		if (value === undefined || value === null) {
			return true;
		}
		if (value.length && value.length === 0) {
			return true;
		}
		if (typeof value === 'string' && value.trim() === '') {
			return true;
		}
		if (typeof value === 'object' && value instanceof Date) {
			return false;
		}
		if (typeof value === 'object' && Object.keys(value).length === 0) {
			return true;
		}
		return false;
	} catch {
		return false;
	}
}
