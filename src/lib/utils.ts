export function cl(...classes: (string | undefined)[]): string {
    return classes.filter(Boolean).join(" ");
}
