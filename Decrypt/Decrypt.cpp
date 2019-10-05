#include<iostream>
#include<iomanip>
#include<string>
#include<algorithm>
#include<math.h>
#include <vector>

using namespace std;

void caesar(string cipher, int key)
{
	int size = cipher.length();
	for (int i = 0; i < size; i++)
	{
		if (cipher[i] - 'A' < 0 || cipher[i] - 'A' > 25)
			cout << cipher[i];
		else
			cout << (char)tolower((cipher[i] - 'A' - key < 0 ? cipher[i] + ('Z' - 'A' + 1) - key : cipher[i] - key));
	}
}

void playfair(string cipher, string key)
{
	int c_size = cipher.length(), k_size = key.length(), index = 0;
	int in_key[26];
	for (int i = 0; i < 26; i++)
		in_key[i] = -1;

	char arr[5][5] = { 0 };

	for (int i = 0; i < c_size; i++)
		if (cipher[i] == 'J')
			cipher[i] = 'I';
	for (int i = 0; i < k_size; i++)
		if (key[i] == 'J')
			key[i] = 'I';
	in_key['J' - 'A'] = 1;

	for (int i = 0; i < k_size; i++)
	{
		if (in_key[key[i] - 'A'] == -1)
		{
			in_key[key[i] - 'A'] = index;
			arr[index / 5][index % 5] = key[i];
			if (++index == 26) break;
		}
	}

	for (int i = 0; i < 26 && index < 26; i++)
	{
		if (in_key[i] == -1)
		{
			in_key[i] = index;
			arr[index / 5][index % 5] = i + 'A';
			index++;
		}
	}

	for (int i = 0; i < c_size; i += 2)
	{
		char first = cipher[i], second = cipher[i + 1];
		int f_key = in_key[first - 'A'], s_key = in_key[second - 'A'];

		if (f_key / 5 == s_key / 5)
			cout << (char)tolower(arr[f_key / 5][(f_key + 4) % 5]) << (char)tolower(arr[f_key / 5][(s_key + 4) % 5]);
		else if (f_key % 5 == s_key % 5)
			cout << (char)tolower(arr[((f_key / 5) + 4) % 5][f_key % 5]) << (char)tolower(arr[((s_key / 5) + 4) % 5][f_key % 5]);
		else
			cout << (char)tolower(arr[f_key / 5][s_key % 5]) << (char)tolower(arr[s_key / 5][f_key % 5]);
	}

}

void vernam(string cipher, string key)
{
	while (cipher.length() > key.length())
		key = key + key;

	for (int i = 0; i < cipher.length(); i++)
		cout << (char)tolower(((cipher[i] - 'A') ^ (key[i] - 'A')) + 'a');
}

void row(string cipher, string key)
{
	int* newkey = new int[key.length()], k_size = key.length(), c_size = cipher.length();
	char* plain = new char[cipher.length()];

	for (int i = 0; i < k_size; i++)
		newkey[i] = key.find((char)(i + '1'));

	int r = 0, c = 0;
	for (int i = 0; i < c_size; i++)
	{
		if (k_size * c + newkey[r] >= c_size)
		{
			r++;
			c = 0;
		}
		plain[k_size * c + newkey[r]] = tolower(cipher[i]);
		c++;
	}

	for (int i = 0; i < c_size; i++)
		cout << plain[i];
}

struct new_pair
{
	int first;
	int second;
	char data;
};

bool first(new_pair a, new_pair b)
{
	if (a.first == b.first) return a.second < b.second;
	return a.first < b.first;
}

bool second(new_pair a, new_pair b)
{
	if (a.second == b.second) return a.first < b.first;
	return a.second < b.second;
}

void rail_fence(string cipher, int key)
{
	int c_size = cipher.length();
	vector<new_pair> p(c_size);
	int row;
	for (size_t i = 0; i < c_size; i++)
	{
		int info = i % (key * 2 - 2);
		row = info < key ? info : (key * 2 - 2) - info;
		p[i].first = row;
		p[i].second = i;
	}

	sort(p.begin(), p.end(), first);
	for (int i = 0; i < c_size; i++)
		p[i].data = cipher[i];

	sort(p.begin(), p.end(), second);
	for (int i = 0; i < c_size; i++)
		cout << (char)tolower(p[i].data);
	p.clear();
}

int main(int argc , char *argv[])
{
	string ciphertext = argv[3], method = argv[1], key=argv[2];

	//cin >> method >> key >> ciphertext;

	if (method == "caesar")
	{
		caesar(ciphertext, atoi(key.c_str()));
	}
	else if (method == "playfair")
	{
		playfair(ciphertext, key);
	}
	else if (method == "vernam")
	{
		vernam(ciphertext, key);
	}
	else if (method == "row")
	{
		row(ciphertext, key);
	}
	else if (method == "rail_fence")
	{
		rail_fence(ciphertext, atoi(key.c_str()));
	}
}