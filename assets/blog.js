/* Sadece posts/ klasörüne .md dosyası ekle; liste otomatik oluşur. */
const BLOG_REPO = 'nullnode1/nullnode1.github.io';
const BLOG_BRANCH = 'main';

function postMeta(file) {
  const slug = file.name.replace(/\.md$/i, '');
  const parts = /^(\d{4})-(\d{2})-(\d{2})-(.+)$/.exec(slug);
  const title = (parts ? parts[4] : slug)
    .replace(/[-_]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return {
    slug,
    fileName: file.name,
    title: title.charAt(0).toLocaleUpperCase('tr-TR') + title.slice(1),
    isoDate: parts ? `${parts[1]}-${parts[2]}-${parts[3]}` : '',
    date: parts ? `${parts[3]}.${parts[2]}.${parts[1]}` : ''
  };
}

let postLoadId = 0;

async function loadPosts() {
  const container = document.querySelector('#post-list');
  if (!container) return;
  const thisLoad = ++postLoadId;
  container.textContent = 'Yazılar yükleniyor…';

  const url = `https://api.github.com/repos/${BLOG_REPO}/contents/posts?ref=${encodeURIComponent(BLOG_BRANCH)}`;
  try {
    const response = await fetch(url, {
      headers: { 'Accept': 'application/vnd.github+json' }
    });
    if (!response.ok) {
      throw new Error(response.status === 403 || response.status === 429
        ? 'GitHub API erişim sınırına ulaşıldı. Biraz sonra tekrar dene.'
        : 'Yazılar alınamadı.');
    }
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Yazı listesi okunamadı.');
    if (thisLoad !== postLoadId || !container.isConnected) return;

    const posts = data
      .filter(file => file.type === 'file' && /\.md$/i.test(file.name))
      .map(postMeta)
      .sort((a, b) => b.fileName.localeCompare(a.fileName, 'tr'));

    if (!posts.length) {
      container.textContent = 'Henüz yayımlanmış bir yazı yok.';
      return;
    }

    const list = document.createElement('ul');
    list.className = 'post-list';
    for (const post of posts) {
      const item = document.createElement('li');
      item.className = 'post-item';
      const link = document.createElement('a');
      link.href = '#/posts/' + encodeURIComponent(post.slug);
      link.textContent = post.title;
      item.append(link);
      if (post.date) {
        const time = document.createElement('time');
        time.className = 'post-date';
        time.dateTime = post.isoDate;
        time.textContent = post.date;
        item.append(time);
      }
      list.append(item);
    }
    container.replaceChildren(list);
  } catch (error) {
    if (thisLoad !== postLoadId || !container.isConnected) return;
    container.className = 'post-error';
    container.textContent = error.message || 'Yazılar alınamadı.';
  }
}
window.blogPostPlugin = function (hook) {
  hook.doneEach(function () {
    if (document.getElementById('post-list')) loadPosts();
    else postLoadId++;
  });
};
