/**
 * In-browser DOM Extractor for Self-Healing UI Automation.
 * Fast, lightweight extraction of interactive elements and their structural attributes.
 */
(() => {
    const interactiveQuery = 'button, input, select, textarea, a, label, [role], [tabindex], [data-testid]';
    const elements = Array.from(document.querySelectorAll(interactiveQuery));
    const results = [];

    const sanitizeAttrs = (el) => {
        const attrs = {};
        const allowed = ['name', 'data-testid', 'placeholder', 'aria-label', 'title', 'type', 'href', 'role'];
        for (const attr of el.attributes) {
            const name = attr.name.toLowerCase();
            if (allowed.includes(name) || name.startsWith('data-')) {
                // Skip passwords or sensitive values
                if (el.type === 'password' && (name === 'value' || name === 'placeholder')) {
                    continue;
                }
                attrs[attr.name] = attr.value.substring(0, 150);
            }
        }
        return attrs;
    };

    const generateSelector = (el) => {
        if (el.hasAttribute('data-testid')) {
            return `[data-testid="${el.getAttribute('data-testid')}"]`;
        }
        if (el.id && /^[A-Za-z][A-Za-z0-9_-]*$/.test(el.id)) {
            // Check uniqueness of ID
            if (document.querySelectorAll('#' + CSS.escape(el.id)).length === 1) {
                return '#' + CSS.escape(el.id);
            }
        }
        if (el.name && el.tagName.toLowerCase() === 'input') {
            return `input[name="${CSS.escape(el.name)}"]`;
        }
        // Fallback to role/tag with text or CSS path
        const tag = el.tagName.toLowerCase();
        const text = (el.innerText || el.textContent || '').trim();
        if (text && text.length < 40 && ['button', 'a'].includes(tag)) {
            return `${tag}:has-text("${text.replace(/"/g, '\\"')}")`;
        }
        // Class-based
        if (el.className && typeof el.className === 'string') {
            const firstClass = el.className.trim().split(/\s+/)[0];
            if (firstClass && !firstClass.includes(':')) {
                const sel = `${tag}.${CSS.escape(firstClass)}`;
                if (document.querySelectorAll(sel).length === 1) {
                    return sel;
                }
            }
        }
        // General fallback
        return tag;
    };

    for (const el of elements) {
        // Check visibility
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
            continue;
        }
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) {
            continue;
        }

        const tag = el.tagName.toLowerCase();
        const text = (el.innerText || el.textContent || '').trim();
        const parent = el.parentElement;

        const parentInfo = parent ? {
            tag: parent.tagName.toLowerCase(),
            id: parent.id || '',
            classes: parent.className && typeof parent.className === 'string' ? parent.className.trim().split(/\s+/) : [],
        } : { tag: '', id: '', classes: [] };

        const childTags = Array.from(el.children).map(c => c.tagName.toLowerCase());

        results.push({
            tag_name: tag,
            element_id: el.id || '',
            class_list: el.className && typeof el.className === 'string' ? el.className.trim().split(/\s+/).filter(Boolean) : [],
            inner_text: text.substring(0, 300),
            aria_role: el.getAttribute('role') || '',
            accessible_name: el.getAttribute('aria-label') || el.getAttribute('title') || '',
            input_type: el.getAttribute('type') || '',
            attributes: sanitizeAttrs(el),
            parent_tag: parentInfo.tag,
            parent_id: parentInfo.id,
            parent_classes: parentInfo.classes,
            children_count: el.children.length,
            children_tags: childTags,
            bounding_box: {
                x: rect.x,
                y: rect.y,
                width: rect.width,
                height: rect.height
            },
            generated_selector: generateSelector(el)
        });
    }

    return results;
})();

